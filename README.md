Некоторые сводные наработки по:
 - авиационному процессингу,
 - телематике,
 - телеметрии,
 - логистике.

#### Решения по архитектуре программного обеспечения

В объем данного проекта входит:
 - разработка баз данных (справочные, рабочие и оперативные данные) на внешнем сервере СУБД,
 - разработка прикладного программного обеспечения - утилит и графических оболочек (в части UX/UI) - для работы с ними,
 - администрирование серверов и баз данных на них.

Справочные данные:
  - объекты (аэропорты, аэродромы, авиабазы, взлетные полосы и хелипады),
  - авиакомпании,
  - летательные аппараты

использовались из источников:
 - http://apinfo.ru 
 - http://openflights.org
 - http://www1.ourairport.com/ (в России пока не открывается)
 - http://planelist.net
 - http://www.flightradar24.com
 - https://www.jetphotos.com/

Рабочие данные по авиарейсам загружаются с https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr

Оперативные данные загружаются с первичного оборудования.

Структура хранилища с базами данных - **Снежинка** (в центре - таблицы с рабочими и оперативными данными (рабочими и тестовыми), по краям - таблицы со справочными данными).
Таблицы с тестовыми данными вынесены на другой жесткий диск.
Каскадные правила на обновления и удаление из рабочих и оперативных данных в справочные не применяются, поэтому они могут быть в отдельных базах данных (уточняется в процессе разработки и эксплуатации).
Модель восстановления баз данных - **Полная**, так как в хранимых процедурах используются помеченные транзакции.
Обслуживание баз данных (целостность, индексы, бэкапы) делается обычным способом - на время все действия завершаются до уведомления о возобновлении работы.

 - Сервер СУБД, 
 - Файловый сервер,
 - Терминальный сервер - работают по учеткам Windows без контроллера домена.

Работа возможна в локальной подсети или из внешней сети через терминальный сервер по RDP.
Прикладное программное обеспечение хранится на файловом сервере и дорабатывается в процессе эксплуатации (в части CI/CD) без уведомления его пользователей.
Права пользователей на доступ к базам данных соответсвуют их учеткам Windows.
Для подписания и утверждения внесения изменений в справочные данные предусматривается использование **сертификата (ЭЦП)** на USB-ом токене.

Для обхода попадания на вложенную обработку исключений на клиентах:
 - установить или обновить **Двайвер ODBC для MS SQL** (дистрибутив версии 17 и руководство см. на сервере в папке `Q:\M$_Windows\SQL_Server\Driver ODBC for SQL Server`),
 - поднять **Системный DSN** в источниках данных ODBC (см. "Подключение к БД через системный DSN" на сервере в папке проекта `..\Руководства в картинках`).

(первоначальное, август 2016-го года) `[Рисунок 1]`
![93936369_591194488270382_464298759405174784_n](https://user-images.githubusercontent.com/104857185/167257457-d5fc8393-4bdc-4391-a76d-9b2b73490016.jpg "Решение по архитектуре")

Поправки:
 - С **tk**, **ttk** переделали на **pyQt**,
 - **Gtk** применялся в Linux-е (библиотека **pyGTK** на Windows сейчас не ставится),
 - (*) Сайт на **WEB-сервере** разрабатывается отдельно и в объем данного проекта не входит.

###### Хранение информации в файлах различных типов и их использование `[Рисунок 2]`

![1 001 001](https://user-images.githubusercontent.com/104857185/167037090-9cd548c0-9643-4903-adce-13e2a039226d.jpg)
_Файлы, открываемые только в своем ПО, желательно не использовать_

###### Отчеты по базам данных из Management Studio

![СУБД Полная - Простая - Сжатие - Полная 001 002](https://user-images.githubusercontent.com/37275122/168450352-48a1e7e1-eeb4-4227-b744-2d368fccac32.png)

![СУБД Полная - Простая - Сжатие - Полная 001 003](https://user-images.githubusercontent.com/37275122/168450358-630fa494-2c0f-4bad-afb1-42bdb44325ec.png)

![СУБД Полная - Простая - Сжатие - Полная 001 004](https://user-images.githubusercontent.com/37275122/168450362-8de3b141-e670-4067-a28e-544cd9cff239.png)

![СУБД Полная - Простая - Сжатие - Полная 001 005](https://user-images.githubusercontent.com/37275122/168890832-25179657-69dd-47e9-8bac-63e5ac56715e.png)

Выпуск релизов и пакетов не предусматривается, так как программное обеспечение на распространяется. 

#### Решения по прикладному программному обеспечению

Летательный аппарат однозначно определяется только сочетанием его заводских номеров (LN, MSN, SN, CN и другие) в зависимости от фирмы-изготовителя.
Регистрационный номер летательного аппарата (англ. _Tail Number_, далее по тексту **регистрация**) с течением времени последовательно меняет несколько летательных аппаратов.
В рабочих и оперативных данных указывается:
 - регистрация,
 - дата авиарейса,
 - строка авиарейса,
 - код IATA объекта отправки,
 - код IATA объекта прилета и остальные данные.
 
Уход от взаимоблокировок при загрузке рабочих и оперативных данных с нескольких внешних клиентов на сервер СУБД выполняется обертыванием тела цикла попыток с нарастающей задержкой по времени в обработку исключения, так как сервер СУБД не дает обратные вызовы (вэб-хуки или программные прерывания) клиентам на повторную попытку, если запрашиваемые данные пока заняты. Без обратных вызовов пока не получается эффективно задействовать внешний сервер СУБД. Транзакции сделаны короткими, но между ними все перезапрашивается снова, так как данные изменяются другими клиентами. Потери времени на задержках частично уменьшены путем уточнения уровня изоляции транзакции в зависимости от действия. Число перезапросов и их перенос по времени пишутся в журнал загрузки рабочих данных (см. `LogReport_DBNew6.txt` в папке проекта на сервере, `ErrorLog.txt` там же - ошибки дозаписи в него). Начальное значение задержки по времени и шаг ее приращения подобран экспериментально по результатам нагрузочных тестов осенью 2019-го года и зависит от вычислительных характеристик сервера СУБД. При 2-х кратном увеличении количества клиентов задержки увеличиваются на 15 ... 20 %, а нагрузка на сервер СУБД (процессор, HDD) уменьшается на 25 ... 35 % благодаря удачно проиндексированным полям в таблицах. Траффик по локальной подсети увеличивается из-за перезапросов. Пропускная способность локальной подсети достаточная.

Каждый клиент использует непрерывное подключение с несколькими клиентскими статическими однопроходными непрокручиваемыми API-курсорами ODBC. При вызове хранимой процедуры используются серверные курсоры. Но хранимые процедуры применяются мало, потому что по мере усложнения прикладного функционала выполнить его только средствами SQL сложно (бедность типов данных и синтаксиса, сложность передачи и возврата составных типов данных, пока нет способа возврата результата и причины несработки). Уровни изоляции транзакции курсоров уточнены и проверены под нагрузкой на 4-х тестовых базах данных летом и осенью 2019-го года.

Контроль подключения и его восстановление при разрыве (например, при плохом контакте на коннекторах, через Wi-Fi или через мобильный Интернет) не предусматривается.

Считаем, что:
 - авиарейс может выполнять собственно авиакомпания-владелец (нет оператора, нет аренды, нет лизинга),
 - авиарейс может выполнять авиакомпания-оператор на летательном аппарате авиакомпании-владельца (нет аренды и нет лизинга),
 - авиарейс может выполнять авиакомпания-оператор на летательном аппарате авиакомпании-арендатора (нет лизинга),
 - авиарейс может выполнять авиакомпания-оператор на летательном аппарате авиакомпании-арендатора, арендодатель которой взял его в лизинг,
 - любая авиакомпания (в том числе неизвестный частный владелец `IATA - пусто`, `ICAO - None`) может быть оператором, владельцем, арендодателем или лизингодателем.
 - начало временного диапазона со следующей регистрацией или в следующей авиакомпании совпадает с окончанием временного диапазона использования в предыдущей.

В базе данных летательных аппаратов:
 - версии 3 ... 5 регистрация и авиакомпании не указаны,
 - версии 6 записываются крайняя регистрация и крайняя авиакомпания-оператор,
 - версии 7 хронология регистраций сделана по принципу _медленно меняющейся размерности_ через отдельную таблицу справочных данных (бизнес-ключ - сочетание заводских номеров, суррогатный ключ -  регистрация по периодам использования соответственно), 
 - версии 7 хронология авиакомпаний сделана по принципу _медленно меняющейся размерности_ через отдельную таблицу справочных данных (бизнес-ключ - сочетание заводских номеров, суррогатные ключи -  авиакомпании по периодам использования соответственно), 
 - версии 8 хронология регистраций и авиакомпаний указывается дополнительно в XML-ных полях.

Чтобы парсить поля **XML(CONTENT dbo.XSD-схема)** как **SAX**, используются комплектные с **MS SQL** функционал **XPath & XQuery** и спецификация **SQL/XML**.
Вставка новой строки или обновление существующей строки вынесена в хранимую процедуру с помеченными транзакциями вместе с частью на XPath & XQuery.
В метках транзакций указываются ...
Все XML-ные поля подаются на вход хранимой процедуре через одну XSD-схему (имя корневого тэга соответствует имени элемента XSD-схемы) за один раз.
Типы данных XML указаны в пространстве имен (см. объявление в XSD-схеме).
Может быть только один тэг с аттрибутом-строкой, обозначающим какую-то одну регистрацию.
Может быть только один тэг с аттрибутом-идентификатором, указывающим на какую-то одну авиакомпанию.
Аттрибуты-идентификаторы в разных XML-ных полях могут указывать на одну и ту же авиакомпанию (см. раздел "Считаем, что ..." выше).
В соответствии с этим относительно корневого тэга вставляются новый тэг и новый подтэг или в существующий тэг вставляется новый подтэг в соответствии с хронологией.
Убирается предыдущий подтэг, если он переходит не в начало временного диапазона в данной авиакомпании. 
Или ничего не меняется, если дата авиарейса попадает в существующий период использования в данной авиакомпании. 
Загрузка рабочих и оперативных данных выполняется в отдельном потоке и не требует соответствия хронологии.

Недостаток хранимой процедуры - не возвращает в скрипты на Python-е результат своей работы (получилось, не получилось с указанием причины).
Недостаток XSD-схемы - тот же и тот, что она пропускает все или не пропускает ничего.

###### Делаем **XML**-ные поля (сделать поля, как написано выше)

![Таблица с полем типа xml с привязкой к схеме xsd](https://user-images.githubusercontent.com/104857185/167261417-e0820f3d-965f-4124-9af6-e59994e09f46.png)

###### Делаем **XSD-схему** и привязываем ее ко всем **XML**-ным полям 

![SSMS - XML-код - Создать схему](https://user-images.githubusercontent.com/104857185/167261451-a42a0c66-2888-4042-88a2-679f1ef6549a.png)

_Поправка по терминологии:
То, что в Management Studio называется **коллекцией схем XML**, точнее называть XSD-схемой. Понимает только файл `*.xsd`. В одной XSD-схеме несколько элементов со своими именами. Пространство имен одно на все элементы XSD-схемы (см. https://www.w3schools.com/xml/schema_simple.asp и https://www.w3.org/TR/xmlschema11-1/). Генерируется из XML внутри Management Studio или с помощью XSLT-преобразования из файла `*.xslt`. Добавляется скриптом._
 
#### Доработки.

Сделать графическую формочку для правки свойств альянсов (или делать это внутри Management Studio). Добавить ссылку на каждый в Wikipedia.

Сделать графическую формочку для правки свойств летательных аппаратов и уточнить набор виджетов на ней, ссылаться на их фото на https://www.jetphotos.com (присутствуют немодерирруемые несоответствия).

Добавить на графической формочке свойств объектов поиск по названию объекта в выпадающем списке с автодополнением из уже имеющихся названий объектов в базе данных, добавить виджеты на вкладке ВПП (широта, долгота, абсолютная отметка, длина, ширина, покрытие полос, оснащение системой сближения и посадки и т. д.), ссылку по объекту на статью в Wikipedia.

Добавить возможность разрешения на внесение изменений в базы данных исполнителями через удостоверение пользователей по ЭЦП, а также подписание извещения на внесение изменений перед их внесением главным специалистом **сертификатом (ЭЦП)** на USB-ом токене. Предусмотреть возможность вывода истории внесения изменений с указанием подписантов (требуются **DDK** или **SDK** от фирмы-изготовителя USB-вых токенов для добавления диалога открытия содержимого токена и выбора на нем требуемого сертификата в пользовательском режиме).

На сайте (см. (*) выше) показать маршруты в виде их профилей на топологии с привязкой к карте на https://www.google.com/maps .

Доработать асинхронную загрузку оперативных данных на API-шках по ВЭБ-хукам с http://www.flightradar24.com и с первичного оборудования.

Проанализировать базы данных с целью дальнейшего улучшения ее производительности с нескольких клиентов в локальной подсети.
 
----
Остальные замечания см. в исходниках по тэгам **todo** и **fixme**
