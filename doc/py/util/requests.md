# Работа с запросами
[Выше](/doc/py/util/index.md) | [Корень](/doc/index.md)

Утилиты для работы с запросами. Описано в [main.util](/main/util.py)

### `getArgumentOr(arr, name, default) -> V (str)|Any`
Возвращает значение аргумента в указанном массиве или стандартное значение при его отсутствии. Как правило имеет тип String
|Параметр |Тип                   |Описание                                                     |
|:--------|:---------------------|:------------------------------------------------------------|
|`arr`    |`dict[K(str), V(str)]`|Карта ключ-значение, в которой будет выполнен поиск аргумента|
|`name`   |`K (str)`             |Название параметра. Как правило имеет тип str                |
|`default`|`Any`                 |Стандартное значение параметра                               |



### `getGetOr(req, name, default) -> V(str)|Any`
Алиас для `getArgumentOr`, где `arr = req.GET`

### `getPostOr(req, name, default) -> V(str)|Any`
Алиас для `getArgumentOr`, где `arr = req.POST`

### `getSessOr(req, name, default) -> V(str)|Any`
Алиас для `getArgumentOr`, где `arr = req.session`

_Автоматически сгенерировано [DocGen](/doc/doc/index.md)_