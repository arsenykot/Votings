# Методы AJAX
[Выше](/doc/js/index.md) | [Корень](/doc/index.md)

Предоставляет методы для работы с AJAX. Функционал реализован в `/main/static/util.js` в регионе `ajax`

### `ajaxQuery(endpoint, method, ready_callback, data, error_passthrough, httpheaders) -> null`
Осуществляет асинхронный запрос на сервер
|Параметр           |Тип                     |Описание                                                                                                                 |
|:------------------|:-----------------------|:------------------------------------------------------------------------------------------------------------------------|
|`endpoint`         |`String`                |Конечная точка API, на которую будет направлен запрос                                                                    |
|`method`           |`"GET"\|"POST"`         |Метод отправляемого запроса                                                                                              |
|`ready_callback`   |`Function[AJAXResponse]`|Метод, который будет вызван по готовности запроса. Должен принимать фиктивный объект AJAXResponse, описанный в примечании|
|`data`             |`Object`                |Тело запроса в виде объекта                                                                                              |
|`error_passthrough`|`Boolean`               |Указывает, попадёт ли ошибка в метод по готовности (по умолчанию - нет)                                                  |
|`httpheaders`      |`Array[Array[String]]`  |Массив пар типа `["ключ", "значение"]`, задающий HTTP-аргументы запроса. По умолчанию пуст                               |



### `ajaxGet(endpoint, ready_callback, data, error_passthrough, httpheaders) -> null`
Алиас для `ajaxQuery`, где `method="GET"`

### `ajaxPost(endpoint, ready_callback, data, error_passthrough, httpheaders) -> null`
Алиас для `ajaxQuery`, где `method="POST"`

### Примечание: Формат фиктивного объекта AJAXResponse
|Поле     |Тип              |Описание                                                                           |
|:--------|:----------------|:----------------------------------------------------------------------------------|
|`status` |`Number\|"error"`|HTTP-статус ответа ИЛИ "error" в случае ошибки, когда `error_passthrough` включено.|
|`content`|`String?`        |Контент ответа на запрос (не существует при `status == "error"`)                   |
|`error`  |`Object?`        |Текст ошибки (не существует при `status != "error"`)                               |


_Автоматически сгенерировано [DocGen](/doc/doc/index.md)_