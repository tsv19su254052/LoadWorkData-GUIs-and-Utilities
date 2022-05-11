# LoadWorkDataAirFlightsDBNew

Некоторые сводные наработки по:
 - авиационному процессингу,
 - телематике,
 - телеметрии,
 - логистике.

Справочные, рабочие и оперативные данные в SQL-ных базах данных **MS SQL Server**-а.

Справочные данные:
  - объекты (аэропорты, аэродромы, авиабазы, взлетные полосы и хелипады),
  - авиакомпании,
  - летательные аппараты

использовались из источников:
 - http://apinfo.ru 
 - http://openflights.org
 - http://www1.ourairport.com/ (в России не открывается)
 - http://planelist.net
 - http://www.flightradar24.com
 - https://www.jetphotos.com/

Рабочие данные по авиаперелетам загружались с https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr

![СУБД Полная - Простая - Сжатие - Полная 001](https://user-images.githubusercontent.com/37275122/167297976-a176bfb8-bdc4-40c5-a0e2-5158ee446ece.png)

Предусматривается:
 - разработка баз данных и администрирование сервера СУБД в Management Studio,
 - работа клиентов на графических формах (UX/UI) только в локальной подсети по учеткам Windows Server-ов без контроллера домена, с заранее заданной конфигурацией сервера СУБД (имена входа, их права) и с ПО в оригинале с файлового сервера, которое дорабатывается в процессе работы (CI/CD) без уведомления клиентов

![93936369_591194488270382_464298759405174784_n](https://user-images.githubusercontent.com/104857185/167257457-d5fc8393-4bdc-4391-a76d-9b2b73490016.jpg "Решение по архитектуре")

----
Для обхода попадания на вложенную обработку исключений на клиентах:
 - при необходимости обновить **двайвер ODBC для MSSQL** до версии 17 (дистрибутив и руководство см. в папке "Q:\M$_Windows\SQL_Server\Driver ODBC for SQL Server").
 - в источниках данных ODBC настроить **Системный DSN** (см. "Подключение к БД через системный DSN" в папке "..\Руководства в картинках"),
 
Уход от взаимоблокировок при загрузке рабочих и оперативных данных на сервер СУБД выполнен с помощью обертывания цикла попыток с нарастающей задержкой в обработку исключения, так как сервер СУБД на дает обратные вызовы (хуки или паузы до прерывания) клиентам на повторную попытку, если запрашиваемые данные пока заняты.

При 2-х кратном увеличении интенсивности запросов или при 3-х кратном увеличении количества клиентов на задержках теряется 15 ... 20 % времени. Нагрузка на сервер СУБД (процесср, HDD) примерно 15 ... 20 % благодаря удачно подобранным индексам с учетом, что пропускная способность локальной подсети достаточная.

Начальное значение задержки по времени и шаг ее приращения подобран экспериментально по результатам нагрузочных тестов осенью 2019-го года и зависит от вычислительных характеристик сервера СУБД, который действует до настоящего времени.

Каждый клиент использует непрерывное подключение с несколькими клиентскими однопроходными статическими непрокручиваемыми API-курсорами ODBC. При вызове хранимой процедуры используются серверные курсоры. Уровени изоляции транзакций курсоров меняются в процессе работы в зависимости от выполняемой операции, которые уточнены и проверены под нагрузкой на 4-х тестовых базах данных летом и осенью 2019-го года.

Контроль подключения и его восстановление при разрыве (например при плохом контакте на коннекторах, через Wi-Fi или через мобильный Интернет) не предусматривается.

Модель восстановления баз данных - **ПОЛНАЯ**, так как в хранимых процедурах используются помеченные транзакции. Обслуживание баз данных (целостность, индексы, бэкапы) делается обычным способом - на время все действия завершаются до уведомления о возобновлении работы.

Загрузка рабочих и оперативных данных выполняется в отдельном потоке.

![1 001 001](https://user-images.githubusercontent.com/104857185/167037090-9cd548c0-9643-4903-adce-13e2a039226d.jpg)

----
Объемы доработок (вступительная часть):
 - Уточнить применение комплектного с **MS SQL** функционала **XPath & XQuery** и комплектной спецификации **SQL/XML**, чтобы нормально парсить XML-ные поля в таблицах баз данных
 - Доработать базу данных по летательным аппаратам таким образом, чтобы писать в нее арендодателей, арендаторов (владельцев) и операторов
в полях **XML(CONTENT dbo.XSD-схема)**, парсить их как **DOM** по веткам и подветкам и при необходимости дописывать подветки по указанному аттрибуту с указанной датой например с помощью хранимой процедуры.
Недостаток хранимой процедуры - не возвращает в скрипты на Python-е результат своей работы (получилось, не получилось с указанием причины).
Недостаток XSD-схемы - тот же и тот, что она пропускает все или не пропускает ничего.

![SSMS - XML-код - Создать схему](https://user-images.githubusercontent.com/104857185/167261451-a42a0c66-2888-4042-88a2-679f1ef6549a.png)
 
![Таблица с полем типа xml с привязкой к схеме xsd](https://user-images.githubusercontent.com/104857185/167261417-e0820f3d-965f-4124-9af6-e59994e09f46.png)

 - Дополнить структуру базы данных по авиакомпаниям (история, владельцы и остальное). Соответственно выбрать способ работы с ними для клиентов. Добавить ссылку на нее с Wikipedia
 - Сделать графическую формочку для правки свойств альянсов (или делать это внутри Management Studio). Добавить ссылку с Wikipedia
 - Сделать графическую формочку для правки свойств летательных аппаратов и уточнить набор виджетов на ней, в том числе их фото (выделить таблицы с мультимедийными полями в отдельную файловую группу, которую вынести на дисковую полку "холодного хранения") или ссылаться на их фото на https://www.jetphotos.com (присутствуют немодерирруемые несоответствия) 
 - Добавить на графической формочке для правки свойств объектов виджеты на вкладке ВПП (широта, долгота, абс. отметка, длина, ширина, покрытие полос, оснащение системой сближения и посадки и т. д.), ссылку по объекту на Wikipedia, поиск по наименованию в виде выпадающего списка (требуется интеграция с поиском Google-а)
 - Добавить возможность разрешения на внесение изменений в базы данных исполнителями через удостоверение пользователей **сертификатом (ЭЦП)** на USB-ом токене, а также подписание извещения на внесение изменений перед их внесением главным специалистом **сертификатом (ЭЦП)** на USB-ом токене. Предусмотреть возможность вывода истории внесения изменений с указанием подписантов (требуются типы данных от фирмы-изготовителя USB-вых токенов для добавления диалога открытия содержимого токена и выбора на нем требуемого сертификата)
 - Дополнить данные по маршрутам их профилями и топологиями с привязкой к картам Google, а также их изменениями с течением времени
 - Разработать асинхронную загрузку оперативных данных на API-шках по ВЭБ-хукам с http://www.flightradar24.com и с первичного оборудования
 - Выполнить визуализацию части данных на ВЭБ-сайте ВЭБ-сервера в этой же локальной подсети
 - Проанализировать базы данных с целью дальнейшего улучшения ее производительности при увеличении количества запросов с нескольких клиентов в локальной подсети

----
Примечания:
 - Остальные замечания см. в исходниках по тэгам **todo** и **fixme**
 - Многие сайты сделаны без API-шек, поэтому пришлось их парсить


