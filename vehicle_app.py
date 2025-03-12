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
        # self.ui.checkBox.currentIndexChanged.connect(self._initialize_table)
        self.ui.checkBox.currentIndexChanged.connect(self._station_status_date_info)
        self.ui.radioButton.clicked.connect(self._low_category_cars)
        self.ui.radioButton.clicked.connect(self._new_cars)
        
        # Initialize the teacher menu and the student table.
        self._low_category_cars()
        self._new_cars()
        self._station_status_date_info()
        
    def show_results(self):
        """
        Show this dialog.
        """
        self.ui.show()
    
    def _low_category_cars(self):
        """
        
        """
        conn = db_connection(config_file = 'querycrew.ini')
        cursor = conn.cursor()
        
        sql = ( 
        """
        #displaying all of the cars that have low price category
        USE querycrew_db;
        SELECT vin, model_year, make, model, price_category
        FROM vehicle_transformed
        WHERE price_category = 'Low'
        ORDER BY model_year;       
        """
        )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
            
        cursor.close()
        conn.close()

        # Set the menu items to the students' names.
        # for row in rows:
        #     name = row[0] + ' ' + row[1]
        #     self.ui.Cars_Info.addItem(row) 

        self.Cars_Info.clear()
        
        for row in rows:
            self.Cars_Info.addItem(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

    def _new_cars(self):
        conn = db_connection(config_file = 'querycrew.ini')
        cursor = conn.cursor()
        
        sql = ( 
            """
            #This is going to give all the newer cars
            USE querycrew_db;
            SELECT vin, model_year, make, model, price_category
            FROM vehicle_transformed
            WHERE model_year > 2022
            ORDER BY model_year;       
            """
        )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
            
        cursor.close()
        conn.close()

        # Set the menu items to the students' names.
        # for row in rows:
        #     name = row[0] + ' ' + row[1]
        #     self.ui.Cars_Info.addItem(row)  
        self.Cars_Info.clear()
        
        for row in rows:
            self.Cars_Info.addItem(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

    def _station_status_date_info(self):
        conn = db_connection(config_file = 'querycrew.ini')
        cursor = conn.cursor()
        
        sql = ( 
            """
            SELECT s.station_name, vi.status AS status, vi.date AS date
            FROM vehicle_inspection vi
            JOIN station s on s.station_id = vi.station_id      
            """
        )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
            
        cursor.close()
        conn.close()

        # Set the menu items to the students' names.
        # for row in rows:
        #     name = row[0] + ' ' + row[1]
        #     self.ui.Station_Info.addItem(row)  

        self.Station_Info.clear()
        
        for row in rows:
            self.Station_Info.addItem(f"{row[0]} - {row[1]} - {row[2]}")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = VehicleApp()
    form.show_results()
    sys.exit(app.exec_())        
