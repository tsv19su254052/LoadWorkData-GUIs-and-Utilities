# LoadWorkDataAirFlightsDBNew

#### Описание
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

Рабочие данные по авиарейсам загружались с https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr

###### Решение по архитектуре программного обеспечения (первоначальное, август 2016-го года) `[Рисунок 1]`

![93936369_591194488270382_464298759405174784_n](https://user-images.githubusercontent.com/104857185/167257457-d5fc8393-4bdc-4391-a76d-9b2b73490016.jpg "Решение по архитектуре")
Поправки:
 - С **tk** и с **ttk** переделали на **pyQt**,
 - **Gtk** применялся в Linux-е (библиотека **pyGTK** на Windows сейчас не ставится),
 - (*) Сайт на **WEB-сервере** разрабатывается отдельно и в объем данного проекта не входит.

###### Хранение информации в файлах различных типов и их использование `[Рисунок 2]`

![1 001 001](https://user-images.githubusercontent.com/104857185/167037090-9cd548c0-9643-4903-adce-13e2a039226d.jpg)
_Файлы, открываемые только в своем ПО, желательно не использовать_

----
#### Назначение:
 - разработка баз данных и администрирование сервера СУБД с помощью **Management Studio (SSMS)**,
 - работа клиентов на графических формах (в части UX/UI) в локальной подсети или через RDP из внешней сети по учеткам Windows Server-ов без контроллера домена с заранее заданной конфигурацией сервера СУБД (имена входа, их права) и с ПО в оригинале на файловом сервере, которое дорабатывается в процессе (в части CI/CD) без уведомления клиентов.

###### Отчеты по базам данных из Management Studio

![СУБД Полная - Простая - Сжатие - Полная 001 002](https://user-images.githubusercontent.com/37275122/168450352-48a1e7e1-eeb4-4227-b744-2d368fccac32.png)

![СУБД Полная - Простая - Сжатие - Полная 001 003](https://user-images.githubusercontent.com/37275122/168450358-630fa494-2c0f-4bad-afb1-42bdb44325ec.png)

![СУБД Полная - Простая - Сжатие - Полная 001 004](https://user-images.githubusercontent.com/37275122/168450362-8de3b141-e670-4067-a28e-544cd9cff239.png)

![СУБД Полная - Простая - Сжатие - Полная 001 005](https://user-images.githubusercontent.com/37275122/168890832-25179657-69dd-47e9-8bac-63e5ac56715e.png)

----
Для обхода попадания на вложенную обработку исключений на клиентах:
 - при необходимости установить или обновить **Двайвер ODBC для MS SQL** (дистрибутив версии 17 и руководство см. на сервере в папке `Q:\M$_Windows\SQL_Server\Driver ODBC for SQL Server`),
 - в источниках данных ODBC поднять **Системный DSN** (см. "Подключение к БД через системный DSN" на сервере в папке проекта `..\Руководства в картинках`).
 
Уход от взаимоблокировок при загрузке рабочих и оперативных данных с нескольких внешних клиентов на сервер СУБД выполняется обертыванием тела цикла попыток с нарастающей задержкой по времени в обработку исключения, так как сервер СУБД не дает обратные вызовы (вэб-хуки или программные прерывания) клиентам на повторную попытку, если запрашиваемые данные пока заняты. Без обратных вызовов пока не получается эффективно задействовать внешний сервер СУБД. Транзакции сделаны короткими, но между ними все перезапрашивается снова, так как данные изменяются другими клиентами. Потери времени на задержках частично уменьшены путем уточнения уровня изоляции транзакции в зависимости от действия. Число перезапросов и их перенос по времени пишутся в журнал загрузки рабочих данных (см. `LogReport_DBNew6.txt` в папке проекта на сервере, `ErrorLog.txt` там же - ошибки дозаписи в него). Начальное значение задержки по времени и шаг ее приращения подобран экспериментально по результатам нагрузочных тестов осенью 2019-го года и зависит от вычислительных характеристик сервера СУБД. При 2-х кратном увеличении количества клиентов задержки увеличиваются на 15 ... 20 %, а нагрузка на сервер СУБД (процессор, HDD) уменьшается на 25 ... 35 % благодаря удачно проиндексированным полям в таблицах. Траффик по локальной подсети увеличивается из-за перезапросов. Пропускная способность локальной подсети достаточная.

Каждый клиент использует непрерывное подключение с несколькими клиентскими статическими однопроходными непрокручиваемыми API-курсорами ODBC. При вызове хранимой процедуры используются серверные курсоры. Но хранимые процедуры применяются мало, потому что по мере усложнения прикладного функционала выполнить его только средствами SQL сложно (бедность типов данных и синтаксиса, сложность передачи и возврата составных типов данных, пока нет способа возврата результата и причины несработки). Уровни изоляции транзакции курсоров уточнены и проверены под нагрузкой на 4-х тестовых базах данных летом и осенью 2019-го года.

Контроль подключения и его восстановление при разрыве (например, при плохом контакте на коннекторах, через Wi-Fi или через мобильный Интернет) не предусматривается.

Структура хранилища с базами данных - **Снежинка**. В центре - таблицы с рабочими и оперативными данными, по краям - таблицы со справочными данными, которые ссылаются на таблицы с другими справочными данными. Таблицы с тестовыми рабочими данными вынесены на другой жесткий диск и ссылаются на те же таблицы со справочными данными, что и рабочие. Таблицы могут быть в разных базах данных. Распределение таблиц по базам данных уточняется в процессе разработки и эксплуатации. Каскадные правила на обновления и удаление данных между ними не применяются.

Модель восстановления баз данных - **Полная**, так как в хранимых процедурах используются помеченные транзакции. Обслуживание баз данных (целостность, индексы, бэкапы) делается обычным способом - на время все действия завершаются до уведомления о возобновлении работы.

Загрузка рабочих и оперативных данных выполняется в отдельном потоке и не требует соответствия хронологии.

Уточнить использование комплектного с **MS SQL** функционала **XPath & XQuery** и комплектной спецификации **SQL/XML**, чтобы парсить поля **XML(CONTENT dbo.XSD-схема)** как **SAX** в базе данных летательных аппаратов для каждого авиарейса следующим образом.

Летательный аппарат однозначно определяется только сочетанием его заводских номеров (LN, MSN, SN, CN и другие) в зависимости от фирмы-изготовителя летательного аппарата.
Регистрационный номер летательного аппарата (англ. _Tail Number_, далее по тексту **регистрация**) с течением времени последовательно меняет несколько летательных аппаратов.
В рабочих и оперативных данных указывается регистрация.

Считаем, что:
 - на одном летательном аппарате один авиарейс например может выполнять авиакомпания-владелец (нет лизинга, нет аренды, нет оператора),
второй авиарейс - авиакомпания-оператор, использующая летательный аппарат авиакомпании-владельца (нет лизинга и нет аренды),
третий авиарейс - авикомпания-оператор на летательном аппарате авиакомпании-арендатора (но без лизинга) и так далее в разных сочетаниях.
 - любая авиакомпания (в том числе неизвестный частный владелец `IATA - пусто`, `ICAO - None`) может быть лизингодателем, арендодателем, владельцем или оператором.
 - начало временного диапазона со следующей регистрацией или в следующей авиакомпании совпадает с окончанием временного диапазона использования в предыдущей.

В базе данных летательных аппаратов:
 - версии 3 ... 5 регистрация и авиакомпании не указаны,
 - версии 6 записаны крайняя регистрация и крайняя авиакомпания,
 - версии 7 хронология регистраций и авиакомпаний сделана по принципу _медленно меняющейся размерности_ через отдельную таблицу справочных данных (бизнес-ключ - сочетание заводских номеров, суррогатный ключ -  регистрации и авиакомпании по периодам использования соответственно), 
 - версии 8 хронология регистраций и авиакомпаний сделана дополнительно указана в XML-ных полях.

Для облегчения отладки выносим вставку новой строки или обновление существующей строки в хранимую процедуру с помеченными транзакциями вместе с частью на XPath & XQuery.
В метках транзакций указываем ...
Все XML-ные поля даем на вход хранимой процедуре через одну XSD-схему (имя корневого тэга соответствует имени элемента XSD-схемы).
Типы данных XML указаны в пространстве имен (см. объявление в XSD-схеме).
Недостаток хранимой процедуры - не возвращает в скрипты на Python-е результат своей работы (получилось, не получилось с указанием причины).
Недостаток XSD-схемы - тот же и тот, что она пропускает все или не пропускает ничего.

Может быть только один тэг с аттрибутом-строкой, обозначающим какую-то одну регистрацию.
Может быть только один тэг с аттрибутом-идентификатором, указывающим на какую-то одну авиакомпанию.
Аттрибуты-идентификаторы в разных XML-ных полях могут указывать на одну и ту же авиакомпанию (см. раздел "Считаем, что ..." выше).

В соответствии с этим вставляем новый тэг и подтэг или вставляем в существующий тэг новый подтэг в соответствии с хронологией.
Убираем предыдущий подтэг, если он переходит не в начало временного диапазона в данной авиакомпании. 
Или ничего не меняем, если дата авиарейса попадает в существующий период использования в данной авиакомпании. 

###### Делаем **XML**-ные поля (сделать поля, как написано выше)

![Таблица с полем типа xml с привязкой к схеме xsd](https://user-images.githubusercontent.com/104857185/167261417-e0820f3d-965f-4124-9af6-e59994e09f46.png)

###### Делаем **XSD-схему** и привязываем ее ко всем **XML**-ным полям 

![SSMS - XML-код - Создать схему](https://user-images.githubusercontent.com/104857185/167261451-a42a0c66-2888-4042-88a2-679f1ef6549a.png)

_Поправка по терминологии:
То, что в Management Studio называется **коллекцией схем XML**, точнее называть XSD-схемой. Понимает только файл `*.xsd`. В одной XSD-схеме несколько элементов со своими именами. Пространство имен одно на все элементы XSD-схемы (см. https://www.w3schools.com/xml/schema_simple.asp и https://www.w3.org/TR/xmlschema11-1/). Генерируется из XML внутри Management Studio или с помощью XSLT-преобразования из файла `*.xslt`. Добавляется скриптом._
 
Сделать графическую формочку для правки свойств альянсов (или делать это внутри Management Studio). Добавить ссылку на каждый в Wikipedia.

Сделать графическую формочку для правки свойств летательных аппаратов и уточнить набор виджетов на ней, ссылаться на их фото на https://www.jetphotos.com (присутствуют немодерирруемые несоответствия).

Добавить на графической формочке свойств объектов поиск по названию объекта в выпадающем списке с автодополнением из уже имеющихся названий объектов в базе данных, добавить виджеты на вкладке ВПП (широта, долгота, абсолютная отметка, длина, ширина, покрытие полос, оснащение системой сближения и посадки и т. д.), ссылку по объекту на статью в Wikipedia.

Добавить возможность разрешения на внесение изменений в базы данных исполнителями через удостоверение пользователей **сертификатом (ЭЦП)** на USB-ом токене, а также подписание извещения на внесение изменений перед их внесением главным специалистом **сертификатом (ЭЦП)** на USB-ом токене. Предусмотреть возможность вывода истории внесения изменений с указанием подписантов (требуются **DDK** или **SDK** от фирмы-изготовителя USB-вых токенов для добавления диалога открытия содержимого токена и выбора на нем требуемого сертификата в пользовательском режиме).

На сайте (* см. выше) показать маршруты в виде их профилей на топологии с привязкой к карте на https://www.google.com/maps .

Разработать асинхронную загрузку оперативных данных на API-шках по ВЭБ-хукам с http://www.flightradar24.com и с первичного оборудования.

Проанализировать базы данных с целью дальнейшего улучшения ее производительности с нескольких клиентов в локальной подсети.
 
----
Остальные замечания см. в исходниках по тэгам **todo** и **fixme**
