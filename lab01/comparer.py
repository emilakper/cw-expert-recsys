def compare_sentiment_results(pizza_result: dict, wizzard_result: dict) -> dict:
    """
    Функция для сравнения сентимент-анализа от PizzaAPI и WizzardAPI.
    Возвращает словарь с результатами сравнения.

    :param pizza_result: Результат от PizzaAPI
    :param wizard_result: Результат от WizardAPI
    :return: Словарь с результатами сравнения
    """
    result = {"pizza_data": {}, "wizzard_data": {}, "comparison": "", "equality": False}

    # Проверка на пустые результаты
    if not pizza_result:
        result["comparison"] = "Text Sentiment Analysis вернул пустой результат."
        return result

    if not wizzard_result:
        result["comparison"] = "Sentiment Analyzer вернул пустой результат."
        return result

    try:
        # Данные из PizzaAPI
        pizza_sentiment = pizza_result.get("sentiment", {})
        result["pizza_data"] = {
            "verdict": pizza_sentiment.get("vote", "unknown").lower(),
            "score": pizza_sentiment.get("score", 0),
            "comparative": pizza_sentiment.get("comparative", 0),
        }

        # Данные из WizzardAPI
        wizzard_sentiment = wizzard_result.get("sentiment", {})
        wizzard_score = wizzard_sentiment.get("score", 0)

        # WizzardAPI не возвращает вердикт в виде слова, описываем сами исходя из score
        if wizzard_score > 0:
            wizzard_verdict = "positive"
        elif wizzard_score < 0:
            wizzard_verdict = "negative"
        else:
            wizzard_verdict = "neutral"

        result["wizzard_data"] = {
            "verdict": wizzard_verdict,
            "score": wizzard_score,
            "positive": wizzard_sentiment.get("pos", 0),
            "negative": wizzard_sentiment.get("neg", 0),
            "neutral": wizzard_sentiment.get("neu", 0),
        }

        pizza_verdict = result["pizza_data"]["verdict"]
        wizzard_verdict = result["wizzard_data"]["verdict"]

        result["equality"] = pizza_verdict == wizzard_verdict

        if result["equality"]:
            result["comparison"] = (
                "Результаты обоих API сходятся: оба дали одинаковую оценку отзыву"
            )
        else:
            result["comparison"] = (
                "Результаты обоих API различаются: сервисы дали разные оценки"
            )

    except Exception as err:
        result["comparison"] = f"Ошибка при обработке результатов: {str(err)}"

    return result


def format_comparison_result(comparison_data: dict) -> str:
    """
    Функция для форматирования результатов сравнения в GUI.

    :param comparison_data: Данные от функции compare_sentiment_results.
    :return: Отформатированная строка с результатами.
    """
    if not comparison_data.get("pizza_data") or not comparison_data.get("wizzard_data"):
        return comparison_data.get("comparison", "Ошибка сравнения")

    output = "============ РЕЗУЛЬТАТЫ АНАЛИЗА ============\n\n"

    # Pizza API
    output += "Text Sentiment Analysis:\n"
    output += f"   Вердикт: {comparison_data['pizza_data']['verdict']}\n"
    output += f"   Общий score: {comparison_data['pizza_data']['score']}\n"
    output += f"   Нормированный score: {comparison_data['pizza_data']['comparative']:.4f}\n\n"

    # Wizard API
    output += "Sentiment Analyzer:\n"
    output += f"   Вердикт: {comparison_data['wizzard_data']['verdict']}\n"
    output += f"   Score: {comparison_data['wizzard_data']['score']:.4f}\n"
    output += f"   Positive: {comparison_data['wizzard_data']['positive']:.3f}\n"
    output += f"   Negative: {comparison_data['wizzard_data']['negative']:.3f}\n"
    output += f"   Neutral: {comparison_data['wizzard_data']['neutral']:.3f}\n\n"

    # Сравнение
    output += "================== ВЫВОД ===================\n"
    output += comparison_data["comparison"]

    return output
