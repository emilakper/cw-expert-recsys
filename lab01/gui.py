import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)
from api_handler import analyze_pizza_api, analyze_wizzard_api
from comparer import compare_sentiment_results, format_comparison_result


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сентимент-анализ отзывов")
        self.setGeometry(100, 100, 800, 600)

        app_font = QApplication.font()
        app_font.setPointSize(12)
        QApplication.setFont(app_font)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Получаем входные данные
        self.input_label = QLabel("Введите текст отзыва:")
        layout.addWidget(self.input_label)

        self.input_text = QTextEdit()
        layout.addWidget(self.input_text)

        # Анализируем
        h_layout = QHBoxLayout()

        self.analyze1_button = QPushButton("Анализ от Text Sentiment analysis")
        self.analyze1_button.clicked.connect(self.analyze_pizza)
        h_layout.addWidget(self.analyze1_button)

        self.analyze2_button = QPushButton("Анализ от Sentiment Analysis")
        self.analyze2_button.clicked.connect(self.analyze_wizzard)
        h_layout.addWidget(self.analyze2_button)

        self.compare_button = QPushButton("Сравнить результаты")
        self.compare_button.clicked.connect(self.compare_results)
        self.compare_button.setEnabled(False)
        h_layout.addWidget(self.compare_button)

        layout.addLayout(h_layout)

        # Вывод результатов
        self.result_label = QLabel("Результаты:")
        layout.addWidget(self.result_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        # Переменные для хранения результатов
        self.pizza_result = None
        self.wizzard_result = None

        central_widget.setLayout(layout)

    def analyze_pizza(self) -> None:
        """
        Функция для анализа текста через Text Sentiment Analysis
        """
        text = self.input_text.toPlainText().strip()

        if not text:
            QMessageBox.warning(self, "Ошибка", "Введите текст для анализа!")
            return

        try:
            self.pizza_result = analyze_pizza_api(text)
            if self.pizza_result:
                verdict = self.pizza_result.get("sentiment", {}).get(
                    "vote", "неизвестно"
                )
                self.result_text.clear()
                self.result_text.append(f"Text Sentiment Analysis: {verdict}")

                if self.wizzard_result:
                    self.compare_button.setEnabled(True)

        except Exception as err:
            self.result_text.append(f"Text Sentiment Analysis: Ошибка {str(err)}")

    def analyze_wizzard(self) -> None:
        """
        Функция для анализа текста через Sentiment Analyzer
        """
        text = self.input_text.toPlainText().strip()

        if not text:
            QMessageBox.warning(self, "Ошибка", "Введите текст для анализа!")
            return

        try:
            self.wizzard_result = analyze_wizzard_api(text)
            if self.wizzard_result:
                score = self.wizzard_result.get("sentiment", {}).get("score", 0)
                self.result_text.clear()
                self.result_text.append(f"Sentiment Analyzer: score = {score:.2f}")

                if self.pizza_result:
                    self.compare_button.setEnabled(True)

        except Exception as err:
            self.result_text.append(f"Sentiment Analyzer: Ошибка {str(err)}")

    def compare_results(self) -> None:
        """
        Функция для сравнения результатов и подробного вывода
        """
        if self.pizza_result and self.wizzard_result:
            self.result_text.clear()
            comparison_data = compare_sentiment_results(
                self.pizza_result, self.wizzard_result
            )
            formatted_result = format_comparison_result(comparison_data)
            self.result_text.append(formatted_result)
        else:
            QMessageBox.warning(self, "Ошибка", "Сначала запустите анализ обоих API!")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
