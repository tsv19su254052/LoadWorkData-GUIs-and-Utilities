# LoadWorkDataAirFlightsDBNew

Некоторые сводные наработки по:
 - авиационному процессингу,
 - телематике,
 - телеметрии.

Справочные, рабочие и оперативные данные в SQL-ных базах данных **MS SQL Server**-а.

Справочные данные:
  - объекты (аэропорты, аэродромы, авиабазы, взлетные полосы и хелипады),
  - авиакомпании,
  - летательные аппараты

использовались в том числе из источников:
 - http://apinfo.ru 
 - http://openflights.org
 - http://www1.ourairport.com/ (в России не открывается)
 - http://planelist.net
 - http://www.flightradar24.com
 - https://www.jetphotos.com/

Рабочие данные по авиаперелетам загружались с таблиц с https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr

Предусматривается:
 - разработка баз данных и администрирование сервера СУБД в Management Studio,
 - работа клиентов через графические формы внутри инфраструктуры по учеткам Windows Server-ов без контроллера домена и с заранее заданной конфигурацией сервера СУБД (имена входа, их права).

![93936369_591194488270382_464298759405174784_n](https://user-images.githubusercontent.com/104857185/167257457-d5fc8393-4bdc-4391-a76d-9b2b73490016.jpg "Решение по архитектуре")

----
Для обхода попадания на обработку вложенных исключений на клиентах:
 - обновить **двайвер ODBC для MSSQL** до версии 17 (дистрибутив и руководство см. в папке "Q:\M$_Windows\SQL_Server\Driver ODBC for SQL Server").
 - настроить в источниках данных **системный DSN** (см. "Подключение к БД через системный DSN" в папке "..\Руководства в картинках"),
 
Уход от взаимоблокировок при чтения/записи СУБД сделан с помощью обертывания цикла попыток с нарастающей задержкой в обработку исключения, так как сервер СУБД на дает обратные вызовы (хуки или паузы до прерывания) клиентам на повторную попытку. При 2-х кратном увеличении интенсивности запросов и при 1.5-х кратном увеличении количества клиентов на задержках теряется 15 ... 20 % времени. Начальное значение задержки по времени и шаг ее приращения подобран экспериментально по результатам тестов и зависит от вычислительных характеристик сервера.

Модель восстановления баз данных - **ПОЛНАЯ**, так как в хранимых процедурах используются помеченные транзакции.

![1 001 001](https://user-images.githubusercontent.com/104857185/167037090-9cd548c0-9643-4903-adce-13e2a039226d.jpg)

----
Дополнительно:
 - Уточнить применение комплектного с **MS SQL** функционала **XPath & XQuery** и комплектной с **MS** спецификации **SQL/XML**, чтобы нормально парсить XML-ные поля в таблицах баз данных
 - Доработать базу по летательным аппаратам таким образом, чтобы писать в нее арендодателей, арендаторов (владельцев) и операторов
в полях **XML(CONTENT XSD-схема)**, парсить их как **DOM** по веткам и подветкам и при необходимости дописывать подветки по указанному аттрибуту с указанной датой например с помощью хранимой процедуры.
Недостаток хранимой процедуры - не возвращает в скрипты на Python-е результат своей работы (получилось, не получилось с указанием причины).
Недостаток XSD-схемы - тот же.

![SSMS - XML-код - Создать схему](https://user-images.githubusercontent.com/104857185/167261451-a42a0c66-2888-4042-88a2-679f1ef6549a.png)
 
![Таблица с полем типа xml с привязкой к схеме xsd](https://user-images.githubusercontent.com/104857185/167261417-e0820f3d-965f-4124-9af6-e59994e09f46.png)

 - Дополнить структуру базы данных по авиакомпаниям (история, владельцы и остальное). Соответственно выбрать способ работы с ними для клиентов. Добавить ссылку на нее с Wikipedia
 - Сделать графическую формочку для правки свойств альянсов (или делать это внутри Management Studio). Добавить ссылку с Wikipedia
 - Сделать графическую формочку для правки свойств летательных аппаратов и уточнить набор виджетов на ней, в том числе их фото, но с выделением таблиц с мультимедийными полями в отдельную файловую группу для вынесения на дисковую полку "холодного хранения" или ссылаться на их фото на https://www.jetphotos.com (присутствуют немодерирруемые несоответствия) 
 - Добавить на графической формочке для правки свойств объектов виджеты на вкладке ВПП (широта, долгота, абс. отметка, длина, ширина, покрытие полос, оснащение системой сближения и посадки и т. д.), ссылку по объекту на Wikipedia, поиск по наименованию в виде выпадающего списка (требуется интеграция с поиском Google-а)
 - Добавить возможность запроса на внесения изменений в базы данных исполнителями через удостоверение пользователей по **сертификату (ЭЦП)** на USB-ом токене (требуются типы данных от фирмы-изготовителя для разработки диалога открытия содержимого токена и выбора на нем требуемого сертификата). Предусмотреть подтверждение изменений перед их внесением главным специалистом. Предусмотреть возможность вывода истории внесения изменений с указанием исполнителей
 - Дополнить данные по маршрутам их профилями и топологиями с привязкой к картам Google, а также их изменениями с течением времени
 - Разработать асинхронную загрузку оперативных данных на API-шках по ВЭБ-хукам с http://www.flightradar24.com
 - Выполнить визуализацию части данных на ВЭБ-сайте

----
Примечания:
 - Остальные замечания см. в исходниках по тэгам **todo** и **fixme**
 - Многие сайты сделаны без API-шек, поэтому пришлось парсить их
