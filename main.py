import sys
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, \
    QTableWidgetItem
from form import Ui_MainWindow


class Film(QWidget):
    def __init__(self):
        super(Film, self).__init__()
        self.setGeometry(350, 200, 275, 175)
        self.setWindowTitle('Фильм')

        self.name = QLabel('Название', self)
        self.name.move(10, 10)
        self.name_input = QLineEdit(self)
        self.name_input.move(120, 10)

        self.year = QLabel('Год выпуска', self)
        self.year.move(10, 40)
        self.year_input = QLineEdit(self)
        self.year_input.move(120, 40)

        self.genre = QLabel('Жанр', self)
        self.genre.move(10, 70)
        self.genre_input = QComboBox(self)
        self.genre_input.move(120, 70)

        self.duration = QLabel('Длительность', self)
        self.duration.move(10, 100)
        self.duration_input = QLineEdit(self)
        self.duration_input.move(120, 100)

        self.confirm = QPushButton('Подтвердить', self)
        self.confirm.move(110, 140)


class Genre(QWidget):
    def __init__(self):
        super(Genre, self).__init__()
        self.setGeometry(350, 200, 275, 80)
        self.setWindowTitle('Фильм')

        self.name = QLabel('Название', self)
        self.name.move(10, 10)
        self.name_input = QLineEdit(self)
        self.name_input.move(120, 10)

        self.confirm = QPushButton('Подтвердить', self)
        self.confirm.move(110, 55)


class MainWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.con = sqlite3.connect('db.db')
        self.cur = self.con.cursor()

        res1 = self.cur.execute('''SELECT * FROM Film''').fetchall()
        res2 = self.cur.execute('''SELECT * FROM Genre''').fetchall()

        self.tableWidget_1.setRowCount(len(res1))
        for i, elem in enumerate(res1):
            for j, val in enumerate(elem):
                self.tableWidget_1.setItem(i, j, QTableWidgetItem(str(val)))

        self.tableWidget_2.setRowCount(len(res2))
        for i, elem in enumerate(res2):
            for j, val in enumerate(elem):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(val)))

        self.stackedWidget.setCurrentIndex(0)
        self.action.triggered.connect(self.change)
        self.btn1_1.clicked.connect(self.add_film)
        self.btn1_2.clicked.connect(self.modify_film)
        self.btn1_3.clicked.connect(self.delete_film)
        self.btn2_1.clicked.connect(self.add_genre)
        self.btn2_2.clicked.connect(self.modify_genre)
        self.btn2_3.clicked.connect(self.delete_genre)

    def change(self):
        names_list = ['Фильмы', 'Жанры']
        cur = abs(self.stackedWidget.currentIndex() - 1)
        self.stackedWidget.setCurrentIndex(cur)
        self.menu.setTitle(self.action.text())
        self.action.setText(names_list[abs(cur - 1)])

    def add_film(self):
        self.label.clear()
        self.film = Film()
        genres = self.cur.execute('''SELECT genre FROM Genre''').fetchall()
        for i in genres:
            for j in i:
                self.film.genre_input.addItem(j)
        self.film.show()
        self.film.confirm.clicked.connect(self.add_film_sql)

    def add_film_sql(self):
        if self.film.year_input.text().isdigit() and self.film.duration_input.text().isdigit():
            list_id = self.cur.execute('''SELECT id FROM Genre WHERE genre = ?''',
                                 (self.film.genre_input.currentText(), )).fetchall()
            id = list_id[0][0]
            self.cur.execute('''INSERT INTO Film(name, year, genre, duration) VALUES(?, ?, ?, ?)''',
                             (self.film.name_input.text(), int(self.film.year_input.text()),
                              id, int(self.film.duration_input.text())))
            res1 = self.cur.execute('''SELECT * FROM Film''').fetchall()
            self.tableWidget_1.setRowCount(len(res1))
            for i, elem in enumerate(res1):
                for j, val in enumerate(elem):
                    self.tableWidget_1.setItem(i, j, QTableWidgetItem(str(val)))
            self.con.commit()
            self.film.hide()
        else:
            self.label.setText('Вы неправильно ввели значения!')

    def modify_film(self):
        self.label.clear()
        if self.tableWidget_1.currentItem() is not None:
            self.film1 = Film()
            genres = self.cur.execute('''SELECT genre FROM Genre''').fetchall()
            for i in genres:
                for j in i:
                    self.film1.genre_input.addItem(j)
            self.values = self.cur.execute('''SELECT * FROM Film WHERE name = ?''',
                                      (self.tableWidget_1.currentItem().text(), )).fetchall()
            self.film1.name_input.setText(self.values[0][1])
            self.film1.year_input.setText(self.values[0][2])
            self.film1.duration_input.setText(str(self.values[0][4]))
            self.film1.show()
            self.film1.confirm.clicked.connect(self.modify_film_sql)
        else:
            self.label.setText('Выбирайте фильм!')

    def modify_film_sql(self):
        if self.film1.year_input.text().isdigit() and self.film1.duration_input.text().isdigit():
            self.cur.execute('''UPDATE Film SET name = ?, year = ?, genre = (SELECT id FROM Genre WHERE genre = ?),
             duration = ? WHERE id = ?''',
                             (self.film1.name_input.text(), int(self.film1.year_input.text()),
                              self.film1.genre_input.currentText(), int(self.film1.duration_input.text()), self.values[0][0]))
            res1 = self.cur.execute('''SELECT * FROM Film''').fetchall()
            self.tableWidget_1.setRowCount(len(res1))
            for i, elem in enumerate(res1):
                for j, val in enumerate(elem):
                    self.tableWidget_1.setItem(i, j, QTableWidgetItem(str(val)))
            self.con.commit()
            self.film1.hide()
        else:
            self.label.setText('Вы неправильно ввели значения!')

    def delete_film(self):
        self.label.clear()
        if self.tableWidget_1.currentItem() is not None:
            self.cur.execute('''DELETE from Film WHERE name = ?''', (self.tableWidget_1.currentItem().text(), ))
            res1 = self.cur.execute('''SELECT * FROM Film''').fetchall()
            self.tableWidget_1.setRowCount(len(res1))
            for i, elem in enumerate(res1):
                for j, val in enumerate(elem):
                    self.tableWidget_1.setItem(i, j, QTableWidgetItem(str(val)))
        else:
            self.label.setText('Выбирайте фильм!')
        self.con.commit()

    def add_genre(self):
        self.label.clear()
        self.genre = Genre()
        self.genre.show()
        self.genre.confirm.clicked.connect(self.add_genre_sql)

    def add_genre_sql(self):
        self.cur.execute('''INSERT INTO Genre(genre) VALUES(?)''',
                         (self.genre.name_input.text(), ))
        res1 = self.cur.execute('''SELECT * FROM Genre''').fetchall()
        self.tableWidget_2.setRowCount(len(res1))
        for i, elem in enumerate(res1):
            for j, val in enumerate(elem):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()
        self.genre.hide()

    def modify_genre(self):
        self.label.clear()
        if self.tableWidget_2.currentItem() is not None:
            self.genre1 = Genre()
            self.values2 = self.cur.execute('''SELECT * FROM Genre WHERE genre = ?''',
                                           (self.tableWidget_2.currentItem().text(), )).fetchall()
            self.genre1.name_input.setText(self.values2[0][1])
            self.genre1.show()
            self.genre1.confirm.clicked.connect(self.modify_genre_sql)
        else:
            self.label.setText('Выбирайте жанр!')

    def modify_genre_sql(self):
        self.cur.execute('''UPDATE Genre SET genre = ? WHERE id = ?''', (self.genre1.name_input.text(), self.values2[0][0]))
        res1 = self.cur.execute('''SELECT * FROM Genre''').fetchall()
        self.tableWidget_2.setRowCount(len(res1))
        for i, elem in enumerate(res1):
            for j, val in enumerate(elem):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(val)))
        self.genre1.hide()
        self.con.commit()

    def delete_genre(self):
        self.label.clear()
        if self.tableWidget_2.currentItem() is not None:
            self.cur.execute('''DELETE from Genre WHERE genre = ?''', (self.tableWidget_2.currentItem().text(), ))
            res1 = self.cur.execute('''SELECT * FROM Genre''').fetchall()
            self.tableWidget_2.setRowCount(len(res1))
            for i, elem in enumerate(res1):
                for j, val in enumerate(elem):
                    self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(val)))
        else:
            self.label.setText('Выбирайте жанр!')
        self.con.commit()

    def closeEvent(self, event):
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec())