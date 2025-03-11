import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView
from connection import db_connection

class VehicleApp(QDialog):
    """
    The student dialog
    """
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi('ev_gui.ui')

        # Student menu and query button event handlers.
        self.ui.checkBox.currentIndexChanged.connect(self._initialize_table)
        self.ui.radioButton.clicked.connect(self._enter_class_data)
        
        # Initialize the teacher menu and the student table.
        self._initialize_student_menu()
        self._initialize_table()
        
    def show_results(self):
        """
        Show this dialog.
        """
        self.ui.show()
    
    def _initialize_student_menu(self):
        """
        Initialize the student menu with student names from the database.
        """
        conn = db_connection(config_file = 'school.ini')
        cursor = conn.cursor()
        
        sql = """
            SELECT first, last FROM student
            ORDER BY last
            """
        
        cursor.execute(sql)
        rows = cursor.fetchall()
            
        cursor.close()
        conn.close()

        # Set the menu items to the students' names.
        for row in rows:
            name = row[0] + ' ' + row[1]
            self.ui.student_menu.addItem(name, row)  
            
    def _adjust_column_widths(self):
        """
        Adjust the column widths of the class table to fit the contents.
        """
        header = self.ui.class_table.horizontalHeader();
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
    def _initialize_table(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.class_table.clear()

        col = ['  Code  ', '   Subject   ']
        self.ui.class_table.setHorizontalHeaderLabels(col)        
        self._adjust_column_widths()
        
    def _enter_class_data(self):    
        """
        Enter class data from the query into 
        the student and takes tables.
        """    
        name = self.ui.student_menu.currentData()
        first_name = name[0]
        last_name = name[1]
        
        conn = db_connection(config_file = 'school.ini')
        cursor = conn.cursor()
        
        sql = ( 
            f"""
            SELECT class.code, class.subject
            FROM student
            JOIN takes
              ON takes.student_id = student.id
            JOIN class
              ON class.code = takes.class_code
            WHERE student.last = '{last_name}'
              AND student.first = '{first_name}'
            ORDER BY class.code
            """ 
              )    
    
        cursor.execute(sql)
        rows = cursor.fetchall()
              
        cursor.close()
        conn.close()
       
        # Set the class data into the table cells.
        row_index = 0
        for row in rows:
            column_index = 0
            
            for data in row:
                item = QTableWidgetItem(str(data))
                self.ui.class_table.setItem(row_index, column_index, item)
                column_index += 1
    
            row_index += 1
               
        self._adjust_column_widths()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = StudentDialog()
    form.show_dialog()
    sys.exit(app.exec_())        