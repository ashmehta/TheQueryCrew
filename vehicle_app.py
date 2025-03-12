import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from connection import db_connection

class VehicleApp(QMainWindow):
    """
    Vehicle Management Application
    """
    def __init__(self):
        """ Load the UI and initialize its components """
        super().__init__()

        # Load the UI
        uic.loadUi('ev_gui.ui', self)

        # Connect the "Run Query" button to the method
        self.pushButton.clicked.connect(self.run_query)

        # Connect checkbox state change to query execution
        self.station_checkBox.stateChanged.connect(self.run_query)  # Updated checkbox name

        # Ensure the tables are cleared at the start
        self.Cars_Info.clearContents()
        self.Station_Info.clearContents()

    def show_results(self):
        """ Show the main window """
        self.show()

    def run_query(self):
        """ Determine which query to execute based on UI selection """

        print("Run Query button clicked!")  # Debugging print

        # Check which radio button or checkbox is selected
        if self.low_price_cat.isChecked():
            print("Fetching Low Price Category Cars...")
            self._low_category_cars()

        elif self.brandNewCars.isChecked():
            print("Fetching New Cars...")
            self._new_cars()

        # Handle station status checkbox separately
        if self.station_checkBox.isChecked():  # Updated checkbox name
            print("Fetching Station Status and Date...")
            self._station_status_date_info()
        else:
            print("Checkbox unchecked, clearing Station_Info table.")
            self.Station_Info.clearContents()
            self.Station_Info.setRowCount(0)

    def _low_category_cars(self):
        """ Fetch low category cars and update the Cars_Info table """
        conn = db_connection(config_file='querycrew.ini')
        cursor = conn.cursor()

        sql = """
        SELECT vin, model_year, make, model, price_category
        FROM vehicle_transformed
        WHERE price_category = 'Low'
        ORDER BY model_year;
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        print(f"Retrieved {len(rows)} rows for Low Price Category Cars.")
        self.update_table(rows, self.Cars_Info)

    def _new_cars(self):
        """ Fetch newer cars and update the Cars_Info table """
        conn = db_connection(config_file='querycrew.ini')
        cursor = conn.cursor()

        sql = """
        SELECT vin, model_year, make, model, price_category
        FROM vehicle_transformed
        WHERE model_year > 2022
        ORDER BY model_year;
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        print(f"Retrieved {len(rows)} rows for New Cars.")
        self.update_table(rows, self.Cars_Info)

    def _station_status_date_info(self):
        """ Fetch station status info and update the Station_Info table """
        conn = db_connection(config_file='querycrew.ini')
        cursor = conn.cursor()

        sql = """
        SELECT s.station_name, vi.status, vi.date
        FROM vehicle_inspection vi
        JOIN station s ON s.station_id = vi.station_id;
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        print(f"Retrieved {len(rows)} rows for Station Status and Date.")
        self.update_table(rows, self.Station_Info)

    def update_table(self, rows, table_widget):
        """ Update the correct QTableWidget with fetched query data """
        table_widget.clearContents()  # Clear previous data
        table_widget.setRowCount(len(rows))  # Set row count
        table_widget.setColumnCount(len(rows[0]) if rows else 0)  # Set column count dynamically

        for row_index, row in enumerate(rows):
            for col_index, data in enumerate(row):
                table_widget.setItem(row_index, col_index, QTableWidgetItem(str(data)))  # Insert data into table

        print("Table updated successfully!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = VehicleApp()
    form.show_results()
    sys.exit(app.exec_())
