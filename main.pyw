import os
import sys
import csv
import datetime
import matplotlib.pyplot as plt
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidget, QApplication, qApp, QPushButton, QLabel, QHBoxLayout,\
    QVBoxLayout, QLineEdit, QCheckBox, QDialog, QMessageBox, QCompleter, QTableWidgetItem, QGroupBox, QScrollArea,\
    QAbstractScrollArea
from PyQt5.QtGui import QPalette, QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry((QApplication.desktop().width() - 600)//2, (QApplication.desktop().height() - 320)//2,
                         600, 320)
        self.setFixedSize(600, 300)
        self.setCentralWidget(MainMenu())
        if no_background is False:
            self.setStyleSheet(".MainWindow{background-image: url('./Data/space.jpg')}")
        self.show()


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        btn_lbl_layout = QHBoxLayout()
        label_layout = QVBoxLayout()
        label_layout_1 = QVBoxLayout()
        button_layout = QVBoxLayout()
        log_layout = QHBoxLayout()
        log_layout_1 = QVBoxLayout()
        
        main_label = QLabel('Spending\ncounter')
        main_label.setStyleSheet('font-size: 40px; font: italic')
        main_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        add_button = QPushButton('New spending')
        add_button.setDefault(True)
        log_button = QPushButton('Show log')
        log_name = QLineEdit()
        log_name.setCompleter(QCompleter(get_names('\\Main_log.csv')))
        log_name.setPlaceholderText('All')
        log_name.textChanged.connect(lambda: log_name.setText(log_name.text().title()))
        log_date = QLineEdit()
        date = str(datetime.date.today()).split('-')
        date = date[1] + '.' + date[0]
        log_date.setPlaceholderText(date)
        quit_button = QPushButton('Quit')

        buttons = []
        for n, label in enumerate(self.get_important_labels()):
            line_layout = QHBoxLayout()
            label_info = self.get_label_information(label)
            label = QLabel(label_info[0])
            label.setAlignment(QtCore.Qt.AlignTop)
            label.setFixedWidth(215)
            if (label_info[1] or label_info[2]) is True:
                label.setStyleSheet('color: red')
            up_label = QPushButton('^')
            up_label.setFixedWidth(20)
            up_label.clicked.connect(lambda: self.move_label(buttons))
            if n == 0:
                up_label.setDisabled(True)
                up_label.setFlat(True)
                up_label.setText('')
            down_label = QPushButton('v')
            down_label.setFixedWidth(20)
            down_label.clicked.connect(lambda: self.move_label(buttons))
            if n == len(self.get_important_labels()) - 1:
                down_label.setDisabled(True)
                down_label.setFlat(True)
                down_label.setText('')
            line_layout.addWidget(label)
            line_layout.addWidget(up_label)
            line_layout.addWidget(down_label)
            label_layout.addLayout(line_layout)
            buttons.append([up_label, down_label])
        label_groupbox = QGroupBox()
        label_groupbox.setLayout(label_layout)
        scroll = QScrollArea()
        scroll.setWidget(label_groupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(250)
        scroll.setFixedWidth(350)
        scroll.setStyleSheet("background-color: transparent")
        label_layout_1.addWidget(scroll)
        edit_button = QPushButton('Edit')
        label_layout_1.addWidget(edit_button)

        log_layout_1.addWidget(log_name)
        log_layout_1.addWidget(log_date)
        log_layout.addLayout(log_layout_1)
        log_layout.addWidget(log_button)

        button_layout.addWidget(main_label)
        button_layout.addWidget(add_button)
        button_layout.addLayout(log_layout)
        button_layout.addWidget(quit_button)
        btn_lbl_layout.addLayout(button_layout)
        btn_lbl_layout.addLayout(label_layout_1)
        layout.addLayout(btn_lbl_layout)
        self.setLayout(layout)

        add_button.clicked.connect(lambda: DateDialog())
        log_button.clicked.connect(lambda: self.show_log(log_name.text(), log_date.text()))
        quit_button.clicked.connect(self.quit_program)
        edit_button.clicked.connect(self.edit)

        self.show()

    @staticmethod
    def get_important_labels():
        labels = []
        log_file = main_folder + '\\Important_categories.csv'
        with open(log_file, newline = '') as log_file:
            reader = csv.reader(log_file, dialect = 'excel')
            for line in reader:
                labels.append(line)
        return labels

    @staticmethod
    def get_label_information(label):
        log_file = main_folder + '\\Main_log.csv'
        with open(log_file, newline = '') as log_file:
            reader = csv.reader(log_file, dialect = 'excel')      
            week_spendings = 0
            month_spendings = 0
            for line in reader:
                if line[0].lower() == label[0].lower():
                    operations = line[2].split('++')
                    for operation in operations:
                        operation_data = operation.split('+')
                        if operation_data == ['']:
                            continue
                        operation_cost = float(operation_data[0])*float(operation_data[1])
                        operation_date = operation_data[2].split('-')
                        for i in range(len(operation_date)):
                            operation_date[i] = int(operation_date[i])
                        operation_date = datetime.date(*operation_date)
                        if (datetime.date.today() - operation_date).days < 7:
                            week_spendings += operation_cost
                        month_spendings += operation_cost
                    if week_spendings > int(label[1]) and int(label[1]) > 0:
                        week_exceeded = True
                    else:
                        week_exceeded = False
                    if month_spendings > int(label[2]) and int(label[2]) > 0:
                        month_exceeded = True
                    else:
                        month_exceeded = False
                    info = [label[0] + ' (' + label[1] + '/week' + '; ' + label[2] + '/month):\n' +
                            str(float('{0:.2f}'.format(week_spendings))) + ' (week); ' +
                            str(float('{0:.2f}'.format(month_spendings))) + ' (month)', week_exceeded, month_exceeded]
                    return info
            info = [label[0] + ' - category not founded', False, False]
            return info
    
    def move_label(self, buttons):
        for i in range(len(buttons)):
            if self.sender() in buttons[i]:
                n = i
        opened_file = main_folder + '\\Important_categories.csv'
        updated_file = main_folder + '\\Important_categories_updated.csv'
        with open(opened_file, newline = '') as infile,\
            open(updated_file, 'w', newline = '') as outfile:
            reader = csv.reader(infile, dialect = 'excel')
            writer = csv.writer(outfile, dialect = 'excel')
            lines = []
            previous_line = ['']
            if self.sender().text() == '^':
                x = n-1
            else:
                x = n
            for i, line in enumerate(reader):
                if i == x:
                    previous_line = line
                    continue
                elif i == x+1:
                    lines.append(line)
                    line = previous_line
                lines.append(line)
            for line in lines:
                writer.writerow(line)
        os.remove(opened_file)
        os.rename(updated_file, opened_file)
        main_window.setCentralWidget(MainMenu())

    @staticmethod
    def show_log(category, period):
        try:
            if period == '':
                period = str(datetime.date.today()).split('-')
                period = period[1] + '.' + period[0]
            if ',' in period:
                period = period.replace(',', '.')
            if '.' in period:
                period = period.split('.')
                period = [datetime.date(int(period[1]), int(period[0]) + 1, 1), 31]
            else:
                period = [datetime.date(int(period) + 1, 1, 1), 365]
            if category in get_names('\\Main_log.csv') or category == '':
                if category == '':
                    category = ' '
                opened_file = main_folder + '\\Main_log.csv'
                with open(opened_file, newline = '') as opened_file_f:
                    reader = csv.reader(opened_file_f, dialect = 'excel')
                    categories = []
                    costs = []
                    for line in reader:
                        if category in line[1].split('+'):
                            categories.append(line[0])
                            cost = 0
                            for transaction in line[2].split('++'):
                                if transaction == '':
                                    continue
                                transaction_data = transaction.split('+')
                                transaction_date = transaction_data[2].split('-')
                                for i in range(len(transaction_date)):
                                    transaction_date[i] = int(transaction_date[i])
                                if (period[0] - datetime.date(*transaction_date)).days > period[1] or \
                                        (period[0] - datetime.date(*transaction_date)).days < 0:
                                    continue
                                cost += float(transaction_data[0]) * float(transaction_data[1])
                            costs.append(cost)
                plt.pie(costs, labels=categories, startangle=90, shadow=True, autopct='%1.1f%%')
                plt.title(category)
                plt.show()
            else:
                raise ValueError

        except ValueError:
            print(period)
            WrongData()

    @staticmethod
    def edit():
        EditImportantLabels()

    @staticmethod
    def quit_program():
        app.quit()


class DateDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(25, 25, 25))
        self.setPalette(palette)
        
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        year = datetime.date.today().year
        month = datetime.date.today().month
        month_name = months[month - 1]
        day = datetime.date.today().day
        current_date = str(day) + ' ' + month_name + ' ' + str(year)
        
        layout = QVBoxLayout()
        date_layout = QHBoxLayout()
        
        btn_layout = QHBoxLayout()
        date_lbl = QLabel('Date:')
        date = QLineEdit()
        date.setPlaceholderText(current_date)
        ok_button = QPushButton('Ok')
        ok_button.setDefault(True)
        cancel_button = QPushButton('Cancel')
        
        date_layout.addWidget(date_lbl)
        date_layout.addWidget(date)
        btn_layout.addWidget(ok_button)
        btn_layout.addWidget(cancel_button)
        layout.addLayout(date_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        ok_button.clicked.connect(lambda: self.clk_button(date_array=date.text().split(),
                                                          months=months, day=day, month=month, year=year))
        cancel_button.clicked.connect(self.clk_button)

        self.exec_()

    def clk_button(self, date_array=None, months=None, day=0, month=0, year=0):
        if date_array is None:
            date_array = []
        if months is None:
            months = []
        sender = self.sender().text()
        correct_data = True
        if sender == 'Ok':
            for i in range(3):
                try:
                    if i == 1:
                        if date_array[1].title() in months:
                            date_array[1] = months.index(date_array[1].title()) + 1
                    date_array[i] = int(date_array[i])
                except IndexError:
                    if i == 0:
                        date_array.append(day)
                    elif i == 1:
                        date_array.append(month)
                    else:
                        date_array.append(year)
                except ValueError:
                    correct_data = False
                    WrongData()
            if correct_data:
                try:
                    datetime.datetime(date_array[2], date_array[1], date_array[0])
                    main_window.setCentralWidget(AddMenu(date_array))
                except ValueError:
                    correct_data = False
                    WrongData()
        if correct_data:
            self.close()


class AddMenu(QWidget):
    def __init__(self, date_array):
        super().__init__()

        self.date_array = date_array
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        name_layout = QHBoxLayout()
        amount_layout = QHBoxLayout()
        price_layout = QHBoxLayout()
        btn_layout = QHBoxLayout()

        main_label = QLabel('New spending')
        main_label.setAlignment(QtCore.Qt.AlignHCenter)
        name_lbl = QLabel('Name')
        self.name = QLineEdit()
        completer = QCompleter(get_names('\\Main_log.csv'))
        completer.setMaxVisibleItems(5)
        self.name.textChanged.connect(lambda: self.find_price(self.name.text()))
        self.name.setCompleter(completer)
        amount_lbl = QLabel('Amount')
        self.amount = QLineEdit()
        self.amount.setPlaceholderText('1')
        price_lbl = QLabel('Price:')
        self.price = QLineEdit()
        self.price_changed = QCheckBox('changed')
        back_button = QPushButton('Back')
        next_button = QPushButton('Next')
        ok_button = QPushButton('Ok')

        name_layout.addWidget(name_lbl)
        name_layout.addWidget(self.name)
        amount_layout.addWidget(amount_lbl)
        amount_layout.addWidget(self.amount)
        price_layout.addWidget(price_lbl)
        price_layout.addWidget(self.price)
        price_layout.addWidget(self.price_changed)
        btn_layout.addWidget(back_button)
        btn_layout.addWidget(next_button)
        btn_layout.addWidget(ok_button)
        layout.addWidget(main_label)
        layout.addLayout(name_layout)
        layout.addLayout(amount_layout)
        layout.addLayout(price_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        back_button.clicked.connect(self.previous_page)
        next_button.clicked.connect(self.next_page)
        ok_button.clicked.connect(self.finish)

        self.show()

        self.data = []
        self.n = 0

    def find_price(self, name):
        self.name.setText(self.name.text().title())
        price = ''
        log_file = main_folder + '\\Main_log.csv'
        with open(log_file, newline = '') as log_file:
            reader = csv.reader(log_file, dialect = 'excel')
            for line in reader:
                if line[0].lower() == name.lower():
                    price = line[3]
        self.price.setPlaceholderText(price)

    def previous_page(self):
        if self.n != 0:
            self.n -= 1
            self.name.setText(self.data[self.n][0])
            self.amount.setText(self.data[self.n][1])
            self.price.setText(self.data[self.n][2])
            if self.data[self.n][3] != 0:
                self.price_changed.setCheckState(True)
            else:
                self.price_changed.setCheckState(False)
            self.data.pop()
        else:
            main_window.setCentralWidget(MainMenu())

    def next_page(self):
        try:
            if self.name.text() != '':
                if self.name.text() not in get_names('\\Main_log.csv'):
                    NewProduct([self.name.text()])
            if self.name.text() != '' and self.name.text() in get_names('\\Main_log.csv'):
                if self.amount.text() == '':
                    self.amount.setText('1')
                if self.price.text() == '':
                    if self.price.placeholderText() == '':
                        self.price.setText('0')
                    else:
                        self.price.setText(self.price.placeholderText())
                self.amount.setText(self.amount.text().replace(',', '.'))
                self.price.setText(self.price.text().replace(',', '.'))
                float(self.amount.text())
                float(self.price.text())
                self.data.append([self.name.text(), self.amount.text(), self.price.text(),
                                  self.price_changed.checkState()])
                self.name.setText('')
                self.amount.setText('')
                self.price.setText('')
                self.price_changed.setCheckState(False)
                self.n += 1
            return True
        except ValueError:
            WrongData()
            return False
            
    def finish(self):
        name = self.name.text()
        if self.next_page() is True and name in get_names('\\Main_log.csv'):
            main_window.setCentralWidget(ChangedMenu(self.date_array, self.data))


class NewProduct(QDialog):
    def __init__(self, names):
        super().__init__()

        self.names = names
        self.init_ui()

    def init_ui(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(25, 25, 25))
        self.setPalette(palette)

        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        parents = []
        for i in range(len(self.names) + 1):
            parents.append(QLineEdit())
            if i < len(self.names):
                parents[i].setText(self.names[i])
                parents[i].setDisabled(True)
            else:
                completer = QCompleter(get_names('\\Main_log.csv'))
                completer.setMaxVisibleItems(5)
                parents[i].setPlaceholderText('Category')
                parents[i].setCompleter(completer)
                parents[i].textChanged.connect(lambda: parents[i].setText(parents[i].text().title()))
            layout.addWidget(parents[i])

        ok_button = QPushButton('Ok')
        cancel_button = QPushButton('Cancel')

        btn_layout.addWidget(ok_button)
        btn_layout.addWidget(cancel_button)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        ok_button.clicked.connect(lambda: self.ok_clicked(parents[i].text()))
        cancel_button.clicked.connect(self.cancel_clicked)

        self.exec_()

    def ok_clicked(self, last_parent):
        parents = last_parent.replace(', ', ',').split(',')
        for parent in parents:
            if parent == '':
                parent = ' '
            self.names.append(parent)
            if parent in get_names('\\Main_log.csv') or parent == ' ':
                
                n = len(self.names)
                
                for i in range(n-1):
                    if self.names[i].title() not in get_names('\\Main_log.csv'):
                        log_file = main_folder + '\\Main_log.csv'
                        with open(log_file, 'a', newline = '') as log_file:
                            writer = csv.writer(log_file, dialect = 'excel')
                            log_file.seek(2)
                            writer.writerow([self.names[i].title(), self.names[i+1].title(), '', ''])
                    else:
                        opened_file = main_folder + '\\Main_log.csv'
                        updated_file = main_folder + '\\Main_log_updated.csv'
                        with open(opened_file, newline = '') as opened_file_f,\
                            open(updated_file, 'w', newline = '') as updated_file_f:
                            reader = csv.reader(opened_file_f, dialect = 'excel')
                            writer = csv.writer(updated_file_f, dialect = 'excel')
                            for line in reader:
                                if line[0].title() == self.names[i].title():
                                    line[1] = line[1] + '+' + self.names[i+1].title()
                                writer.writerow(line)
                        os.remove(opened_file)
                        os.rename(updated_file, opened_file)
            else:
                NewProduct(self.names)
            self.names.pop()
            self.close()

    def cancel_clicked(self):
        self.close()


class ChangedMenu(QWidget):
    def __init__(self, date_array, data):
        super().__init__()

        self.date_array = date_array
        self.data = data
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        main_label = QLabel('Updated spendings')
        main_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.table = QTableWidget(0, 3)
        for i in range(3):
            self.table.setColumnWidth(i, main_window.width()/3 - 14)
        col_headers = ['Product', 'Week', 'Month']
        self.table.setHorizontalHeaderLabels(col_headers)
        button = QPushButton('Close')
        button.setDefault(True)

        layout.addWidget(main_label)
        layout.addWidget(self.table)
        layout.addWidget(button)
        self.setLayout(layout)
        
        self.update_log()
        button.clicked.connect(lambda: main_window.setCentralWidget(MainMenu()))

        self.fill_table()
        self.show()

    def update_log(self):
        transactions = []
        self.updated_names =[]
        for i in range(len(self.data)):
            transactions.append([self.data[i][0], float(self.data[i][1]), float(self.data[i][2]), self.data[i][3]])
            if self.data[i][0] not in self.updated_names:
                self.updated_names.append(self.data[i][0].title())
        log_file = main_folder + '\\Main_log.csv'
        updated_file = main_folder + '\\Main_log_updating.csv'
        with open(log_file, newline = '') as log_file,\
        open(updated_file, 'w', newline = '') as updated_file:
            reader = csv.reader(log_file, dialect = 'excel')
            writer = csv.writer(updated_file, dialect = 'excel')

            i = 0
            n = len(transactions)
            while i < n:
                for line in reader:
                    if line[0].lower() == transactions[i][0].lower():
                        parents = line[1].split('+')
                        for parent in parents:
                            if parent != ' ':
                                transactions.append([parent, transactions[i][1], transactions[i][2], 0])
                                if parent not in self.updated_names:
                                    self.updated_names.append(parent)
                log_file.seek(0)
                n = len(transactions)
                i += 1

            log_file.seek(0)
            for line in reader:
                for transaction in transactions:
                    if line[0].lower() == transaction[0].lower():
                        line[2] = line[2] + '++' + str(transaction[2]) + '+' + str(transaction[1]) + \
                                  '+' + str(self.date_array[2]) + '-' + str(self.date_array[1]) + '-' + \
                                  str(self.date_array[0])
                        if transaction[3] != 0:
                            line[3] = str(transaction[2])
                        transaction = transaction[1:]
                writer.writerow(line)
        log_file = main_folder + '\\Main_log.csv'
        updated_file = main_folder + '\\Main_log_updating.csv'
        os.remove(log_file)
        os.rename(updated_file, log_file)

    def fill_table(self):
        log_file = main_folder + '\\Main_log.csv'
        with open(log_file, newline = '') as log_file:
            reader = csv.reader(log_file, dialect = 'excel')
            self.updated_names.sort()
            for n, name in enumerate(self.updated_names):            
                week_spendings = 0
                month_spendings = 0
                for line in reader:
                    if line[0].lower() == name.lower():
                        operations = line[2].split('++')
                        for operation in operations:
                            operation_data = operation.split('+')
                            if operation_data == ['']:
                                continue
                            operation_cost = float(operation_data[0])*float(operation_data[1])
                            operation_date = operation_data[2].split('-')
                            for i in range(len(operation_date)):
                                operation_date[i] = int(operation_date[i])
                            operation_date = datetime.date(*operation_date)
                            if (datetime.date.today() - operation_date).days < 7:
                                week_spendings += operation_cost
                            if (datetime.date.today() - operation_date).days < 31:
                                month_spendings += operation_cost
                        self.table.insertRow(n)
                        item = QTableWidgetItem(self.updated_names[n])
                        self.table.setItem(n, 0, item)
                        item = QTableWidgetItem(str(float('{0:.2f}'.format(week_spendings))))
                        self.table.setItem(n, 1, item)
                        item = QTableWidgetItem(str(float('{0:.2f}'.format(month_spendings))))
                        self.table.setItem(n, 2, item)
                log_file.seek(0)


class EditImportantLabels(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(25, 25, 25))
        self.setPalette(palette)

        layout = QVBoxLayout()
        name_layout = QHBoxLayout()
        per_week_layout = QHBoxLayout()
        per_month_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        name_lbl = QLabel('Name:')
        self.name = QLineEdit()
        names_raw = get_names('\\Main_log.csv') + get_names('\\Important_categories.csv')
        names = []
        for i in range(len(names_raw)):
            for j in range(1, len(names_raw[i:])):
                if names_raw[i] == names_raw[j+i]:
                    names_raw[j+i] = ''
            if names_raw[i] != '':
                names.append(names_raw[i])
        completer = QCompleter(names)
        completer.setMaxVisibleItems(5)
        self.name.textChanged.connect(self.text_changed)
        self.name.setCompleter(completer)
        per_week_lbl = QLabel('Per week:')
        self.per_week = QLineEdit()
        self.per_week.setPlaceholderText('no limit')
        per_month_lbl = QLabel('Per month:')
        self.per_month = QLineEdit()
        self.per_month.setPlaceholderText('no limit')

        self.add_button = QPushButton('Add')
        self.add_button.setDisabled(True)
        self.remove_button = QPushButton('Remove')
        self.remove_button.setDisabled(True)
        self.edit_button = QPushButton('Edit')
        self.edit_button.setDisabled(True)

        name_layout.addWidget(name_lbl)
        name_layout.addWidget(self.name)
        per_week_layout.addWidget(per_week_lbl)
        per_week_layout.addWidget(self.per_week)
        per_month_layout.addWidget(per_month_lbl)
        per_month_layout.addWidget(self.per_month)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.edit_button)

        layout.addLayout(name_layout)
        layout.addLayout(per_week_layout)
        layout.addLayout(per_month_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_label)
        self.remove_button.clicked.connect(self.remove_edit_label)
        self.edit_button.clicked.connect(self.remove_edit_label)

        self.exec_()

    def text_changed(self):
        self.name.setText(self.name.text().title())
        if self.name.text() in get_names('\\Important_categories.csv'):
            self.add_button.setDisabled(True)
            self.remove_button.setEnabled(True)
            self.edit_button.setEnabled(True)
            self.show_limits()
        else:
            if self.name.text().lower() == '':
                self.add_button.setDisabled(True)
            else:
                self.add_button.setEnabled(True)
            self.remove_button.setDisabled(True)
            self.edit_button.setDisabled(True)
            self.per_week.setPlaceholderText('no limit')
            self.per_month.setPlaceholderText('no limit')

    def show_limits(self):
        opened_file = main_folder + '\\Important_categories.csv'
        with open(opened_file, newline = '') as opened_file:
            reader = csv.reader(opened_file, dialect = 'excel')
            for line in reader:
                if self.name.text().lower() == line[0].lower() and len(line) == 3:
                    if line[1] != '0':
                        limit = line[1] + ' zł'
                        self.per_week.setPlaceholderText(limit)
                    if line[2] != '0':
                        limit = line[2] + ' zł'
                        self.per_month.setPlaceholderText(limit)

    def add_label(self):
        try:
            if self.per_week.text() != '':
                int(self.per_week.text())
            else:
                self.per_week.setText('0')
            if self.per_month.text() != '':
                int(self.per_month.text())
            else:
                self.per_month.setText('0')
            opened_file = main_folder + '\\Important_categories.csv'
            with open(opened_file, 'a', newline = '') as opened_file:
                opened_file.seek(2)
                writer = csv.writer(opened_file, dialect = 'excel')
                writer.writerow([self.name.text().title(), self.per_week.text(), self.per_month.text()])
            main_window.setCentralWidget(MainMenu())
            self.close()
        except ValueError:
            WrongData()

    def remove_edit_label(self):
        try:
            sender = self.sender().text()
            opened_file = main_folder + '\\Important_categories.csv'
            updated_file = main_folder + '\\Important_categories_updated.csv'
            with open(opened_file, newline = '') as opened_file,\
                open(updated_file, 'w', newline = '') as updated_file:
                reader = csv.reader(opened_file, dialect = 'excel')
                writer = csv.writer(updated_file, dialect = 'excel')
                for line in reader:
                    if line[0].lower() == self.name.text().lower():
                        if sender == 'Remove':
                            continue
                        if self.per_week.text() != '':
                            int(self.per_week.text())
                            line[1] = self.per_week.text()
                        if self.per_month.text() != '':
                            int(self.per_month.text())
                            line[2] = self.per_month.text()
                    writer.writerow(line)
            opened_file = main_folder + '\\Important_categories.csv'
            updated_file = main_folder + '\\Important_categories_updated.csv'
            os.remove(opened_file)
            os.rename(updated_file, opened_file)
            main_window.setCentralWidget(MainMenu())
            self.close()
        except ValueError:
            WrongData()


class WrongData(QMessageBox):
    def __init__(self):
        super().__init__()
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(25, 25, 25))
        self.setPalette(palette)
        
        self.setText('Wrong data!')
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle('Error')
        self.setStandardButtons(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
        self.exec_()


def get_names(file_name):
    names = []
    opened_file = main_folder + file_name
    with open(opened_file, newline = '') as opened_file:
        reader = csv.reader(opened_file, dialect = 'excel')
        for line in reader:
            names.append(line[0])
    return names


def files_not_created():
    if main_folder not in os.listdir('./'):
        return ['No folder']
    problems = []
    if 'Main_log.csv' not in os.listdir('./' + main_folder):
        problems.append('No log')
    if 'Important_categories' not in os.listdir('./' + main_folder):
        problems.append('No important categories')
    if 'space.jpg' not in os.listdir('./' + main_folder):
        problems.append('No background')
    return problems


app = QApplication(sys.argv)
main_folder = 'Data'

qApp.setStyle('Fusion')
main_palette = QPalette()
main_palette.setColor(QPalette.WindowText, QtCore.Qt.white)
main_palette.setColor(QPalette.Base, QColor(25, 25, 25))
main_palette.setColor(QPalette.Text, QtCore.Qt.white)
main_palette.setColor(QPalette.Button, QColor(12, 30, 58))
main_palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
main_palette.setColor(QPalette.BrightText, QtCore.Qt.red)

no_background = False
problems = files_not_created()
if 'No folder' in problems:
    os.mkdir(main_folder)
    problems = ['No log', 'No important categories', 'No background']
if 'No log' in problems:
    filename = main_folder + '\\Main_log.csv'
    f = open(filename, 'w')
    f.close()
if 'No important categories' in problems:
    filename = main_folder + '\\Important_categories.csv'
    f = open(filename, 'w')
    f.close()
if 'No background' in problems:
    if 'space.jpg' in os.listdir('./'):
        filename = main_folder + '\\space.jpg'
        os.rename('space.jpg', filename)
    else:
        main_palette.setColor(QPalette.Window, QColor(12, 30, 58))
        no_background = True

app.setPalette(main_palette)

main_window = MainWindow()
sys.exit(app.exec_())
