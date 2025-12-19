# Утилиты для HTML
[Выше](/doc/js/index.md) | [Корень](/doc/index.md)

Предоставляет методы-утилиты для работы с HTML. Функционал реализован в `/main/static/util.js` в регионе `htmlutils`

### `setSpinner(element, text, size, type) -> null`
Заменяет `innerHTML` элемента на спиннер с указанным текстом.
|Параметр |Тип                |Описание                                                                                                                              |
|:--------|:------------------|:-------------------------------------------------------------------------------------------------------------------------------------|
|`element`|`HTMLElement`      |Целевой элемент                                                                                                                       |
|`text`   |`String`           |Текст возле спиннера                                                                                                                  |
|`size`   |`"sm"\|"lg"?`      |Размер спиннера. По умолчанию `sm`. См. [документацию для спиннеров](https://getbootstrap.com/docs/5.3/components/spinners/)          |
|`type`   |`"border"\|"grow"?`|Тип анимации спиннера. По умолчанию `border`. См. [документацию для спиннеров](https://getbootstrap.com/docs/5.3/components/spinners/)|



### `spawnToast(color, icon, content, closeButton, container) -> null`
Создаёт уведомление-тост с указанными параметрами
|Параметр     |Тип          |Описание                                                                                                    |
|:------------|:------------|:-----------------------------------------------------------------------------------------------------------|
|`color`      |`String`     |Цвет уведомления-тоста. См. [Список цветов](https://getbootstrap.com/docs/5.3/customize/color/#theme-colors)|
|`icon`       |`String`     |Название иконки [отсюда](https://icons.getbootstrap.com/)                                                   |
|`content`    |`String`     |HTML-содержимое уведомления-тоста                                                                           |
|`closeButton`|`Boolean`    |Указывает, будет ли видна кнопка закрытия тоста. По умолчанию `false`                                       |
|`container`  |`HTMLElement`|HTML-элемент, в который требуется поместить тост. По умолчанию элемент с ID `toast-container`               |



_Автоматически сгенерировано DocGen из XML-файла docs.xml_

_Структуру файла docs.xml см. в [/DOC.XSD](/DOC.XSD) или [здесь](/doc/doc/index.md)._