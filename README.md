Некоторые сводные наработки по:
 - авиационному процессингу,
 - телеметрии,
 - телематике.

#### Решения по архитектуре программного обеспечения

В объем данного проекта входит:
 - разработка баз данных (справочные, рабочие и оперативные данные) на внешнем сервере СУБД,
 - разработка прикладного программного обеспечения - утилит и графических оболочек (в части UX/UI) - для работы с ними,
 - администрирование серверов и баз данных на них.

Справочные данные:
  - объекты (аэропорты, аэродромы, авиабазы, вертодромы, взлетные полосы и хелипады),
  - авиакомпании,
  - летательные аппараты

использовались из источников:
 - http://apinfo.ru 
 - http://openflights.org
 - http://www1.ourairport.com/
 - http://planelist.net
 - http://www.flightradar24.com
 - https://www.jetphotos.com/

Рабочие данные по авиарейсам загружаются с https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr

Оперативные данные загружаются с первичного оборудования.

Структура хранилища с базами данных - **Снежинка** (в центре - таблицы с рабочими и оперативными данными (рабочими и тестовыми), по краям - таблицы со справочными данными).
Таблицы с тестовыми рабочими данными могут быть вынесены на другой жесткий диск.
Есть таблица, в шапке которой есть справочные поля, ввод в которые делается только вручную по нескольким источникам,
и поля, которые заполняются в процессе загрузки рабочих и оперативных данных.
Модель восстановления баз данных - **Полная**, так как в хранимых процедурах используются помеченные транзакции.
Обслуживание баз данных (целостность, индексы, бэкапы) делается обычным способом - на время все действия завершаются до уведомления о возобновлении работы.

Инфраструктура:
 - сервер СУБД, 
 - файловый сервер,
 - терминальный сервер - работают по учеткам Windows без контроллера домена.

Работа возможна в локальной подсети или из внешней сети через терминальный сервер по RDP.
Прикладное программное обеспечение хранится на файловом сервере и дорабатывается в процессе эксплуатации (в части CI/CD) без уведомления его пользователей.

Права пользователей на доступ к базам данных соответсвуют их учеткам Windows.

(первоначальное, август 2016-го года) `[Рисунок 1]`
![93936369_591194488270382_464298759405174784_n](https://user-images.githubusercontent.com/104857185/167257457-d5fc8393-4bdc-4391-a76d-9b2b73490016.jpg "Решение по архитектуре")

Поправки:
 - С **tk**, **ttk** переделали на **pyQt**,
 - **Gtk** применялся в Linux-е (библиотека **pyGTK** на Windows сейчас не ставится),
 - Linux может использоваться на клиентах для правки справочных данных,
 - (*) Сайт на **WEB-сервере** разрабатывается отдельно и в объем данного проекта не входит.

###### Хранение информации в файлах различных типов и их использование `[Рисунок 2]`

![1 001 001](https://user-images.githubusercontent.com/104857185/167037090-9cd548c0-9643-4903-adce-13e2a039226d.jpg)
_Файлы, открываемые только в своем ПО, желательно не использовать_

###### Отчеты по базам данных из Management Studio

![СУБД Полная - Простая - Сжатие - Полная 001 003](https://user-images.githubusercontent.com/37275122/168450358-630fa494-2c0f-4bad-afb1-42bdb44325ec.png)

![СУБД Полная - Простая - Сжатие - Полная 001 004](https://user-images.githubusercontent.com/37275122/168450362-8de3b141-e670-4067-a28e-544cd9cff239.png)

![СУБД Полная - Простая - Сжатие - Полная 001 005](https://user-images.githubusercontent.com/37275122/168890832-25179657-69dd-47e9-8bac-63e5ac56715e.png)

#### Решения по прикладному программному обеспечению

Летательный аппарат однозначно определяется сочетанием его заводских номеров (LN, MSN, SN, CN и другие) в зависимости от фирмы-изготовителя.

Регистрационный номер летательного аппарата (англ. _Tail Number_, далее по тексту **регистрация**) с течением времени может последовательно менять несколько летательных аппаратов.

В рабочих и оперативных данных указывается:
 - регистрация,
 - дата авиарейса,
 - строка авиарейса,
 - код IATA объекта отправки,
 - код IATA объекта прилета,
 - число ходок с этим авиарейсом
   и остальные данные.
 
Любая авиакомпания (в том числе неизвестный частный владелец `IATA - пусто`, `ICAO - None`) может быть оператором, владельцем (арендатором), арендодателем или лизингодателем.

Считаем, что авиарейс может выполнять:
 - собственно авиакомпания-владелец (нет оператора, нет аренды, нет лизинга),
 - авиакомпания-оператор на летательном аппарате авиакомпании-владельца (нет аренды и нет лизинга),
 - авиакомпания-оператор на летательном аппарате авиакомпании-арендатора (нет лизинга),
 - авиакомпания-оператор на летательном аппарате авиакомпании-арендатора, арендодатель которой взял его в лизинг.

###### Делаем **XML**-ные поля

![SSMS Делаем XML-ные поля](https://user-images.githubusercontent.com/104857185/173250391-229e37c8-c996-4d22-bf0f-7df07d0845b0.png)

_Поправка по терминологии:
То, что в Management Studio называется **коллекцией схем XML**, точнее называть XSD-схемой. К каждому XML-ному полю привязывается своя XSD-схема._

В XML-ном поле регистрации может быть только один тэг с **аттрибутом-строкой**, обозначающим какую-то одну регистрацию.
Начало временного диапазона со следующей регистрацией считаем окончанием временного диапазона использования с предыдущей.
Заполняем только ручным вводом.

В каждом XML-ном поле авиакомпании может быть только один тэг с **аттрибутом-идентификатором**, указывающим на какую-то одну авиакомпанию.
Начало временного диапазона в следующей авиакомпании считаем окончанием временного диапазона использования в предыдущей.
Аттрибуты-идентификаторы в разных XML-ных полях могут указывать на одну и ту же авиакомпанию (см. "Считаем, что ..." выше).
Заполняется при внесении рабочих и оперативных данных.

Вставка новой строки или обновление существующей строки с XML-ными полями вынесена в хранимую процедуру с помеченными транзакциями.
Все XML-ные поля **XML(CONTENT dbo.XSD-схема)** подаются на вход хранимой процедуры через одну XSD-схему и парсятся как **SAX**,
используя комплектный функционал **XPath & XQuery** и спецификацию **SQL/XML**.
Имя корневого тэга XML-ного поля соответствует имени элемента XSD-схемы.
В отметке транзакции указывается ___.

Недостаток хранимой процедуры - не возвращает в скрипты на Python-е результат своей работы (получилось, не получилось с указанием причины).
Недостаток XSD-схемы - тот же и тот, что она пропускает все или не пропускает ничего.

Каждый элемент XSD-схемы генерируется из своего XML-ного поля внутри Management Studio или с помощью XSLT-преобразования из файла `*.xslt`и
вставляется под своим именем по порядку просмотра XML-ных полей в скрипт создания XSD-схемы.

###### Генерируем элемент **XSD-схемы (устарело, как пример)** 

![SSMS - XML-код - Создать схему](https://user-images.githubusercontent.com/104857185/167261451-a42a0c66-2888-4042-88a2-679f1ef6549a.png)

В одной XSD-схеме может быть несколько элементов.
Элементы со своими именами.
К базе данных может быть привязано несколько XSD-схем.
Пространства имен для всех элементов объявляются в начале скрипта создания XSD-схемы (см. https://www.w3schools.com/xml/schema_simple.asp и https://www.w3.org/TR/xmlschema11-1/).
Типы данных, применяемые в XML-ных полях, соответствуют объявленным пространствам имен
(см. https://github.com/tsv19su254052/LoadWorkDataAirFlightsDBNew/blob/master/SQL%20%26%20XML%20(XPath%20%26%20XQuery%20XSD%20XDR%20XSLT)/AirCraftCommonSchemaSourceFull.xsd).
Для создания XSD-схемы открыть и запустить собранный скрипт.

###### Создание схемы из пространств имен и элементов

![XSD-схема Сборка из элементов и пространств имен](https://user-images.githubusercontent.com/37275122/171510416-e57ed19e-71b3-45e5-a6d7-257017b9b786.png)
 
XML-ные поля пропускаются через XSD-схему в следующих случаях:
 - на входе хранимой процедуры,
 - при вставке или обновлении строки,
 - при ручном заполнении XML-ного файла,
 - при ручном вводе XML-ного поля.

В соответствии со всем этим:
 - ищем строки летательных аппаратов и парсим в них XML-ные поля регистрации (первичный XML-ный индекс) по тэгу с аттрибутом-строкой с указанной регистрацией,
 - выбираем из них строку с временным диапазоном, который соответствует дате авиарейса,
 - в каждом XML-ном поле авиакомпании этой строки относительно корневого тэга вставляем новый тэг и новый подтэг
   или в существующий тэг с указанным аттрибутом-идентификатором авиакомпании вставляем новый подтэг,
   убираем предыдущий подтэг, если он переходит не в начало этого временного диапазона
   или ничего не меняем, если дата авиарейса попадает в существующий период.

Если регистрации нет в базе данных:
 - загрузка ставит флаг,
 - недозагруженные данные на время пишутся во временную таблицу по образцу 7-й версии,
 - формируется список регистраций, которые надо восполнить в базе данных,
 - после восполнения они переносятся к остальным данным.

Если в рабочих или оперативных данных не указана регистрация, то в летательные аппараты изменения не вносятся.

Загрузка рабочих и оперативных данных выполняется асинхронно в произвольном порядке в отдельном потоке и не требует соответствия хронологии.

Уход от взаимоблокировок при загрузке рабочих и оперативных данных с нескольких внешних клиентов на сервер СУБД выполняется
обертыванием тела цикла попыток с нарастающей задержкой по времени в обработку исключения,
так как сервер СУБД не дает обратные вызовы (вэб-хуки или программные прерывания) клиентам на повторную попытку, если запрашиваемые данные пока заняты.
Без обратных вызовов пока не получается эффективно задействовать внешний сервер СУБД.
Транзакции сделаны короткими, но между ними все перезапрашивается снова, так как данные изменяются другими клиентами.
Потери времени на задержках частично уменьшены путем уточнения уровня изоляции транзакции в зависимости от действия.
Число перезапросов и их перенос по времени пишутся в журнал загрузки рабочих данных
(см. `LogReport_DBNew6.txt` в папке проекта на сервере, `ErrorLog.txt` там же - ошибки дозаписи в него).
Начальное значение задержки по времени и шаг ее приращения подобран экспериментально по результатам нагрузочных тестов осенью 2019-го года
и зависит от вычислительных характеристик сервера СУБД. При 2-х кратном увеличении количества клиентов задержки увеличиваются на 15 ... 20 %,
а нагрузка на сервер СУБД (процессор, HDD) уменьшается на 25 ... 35 % благодаря удачно проиндексированным полям в таблицах.
Траффик по локальной подсети увеличивается из-за перезапросов. Пропускная способность локальной подсети достаточная.

Каждый клиент использует непрерывное подключение с несколькими клиентскими статическими однопроходными непрокручиваемыми API-курсорами ODBC.
При вызове хранимой процедуры используются серверные курсоры.
Хранимые процедуры применяются мало, потому что по мере усложнения прикладного функционала выполнить его только средствами SQL сложно
(бедность типов данных и синтаксиса, сложность передачи и возврата составных типов данных, пока нет способа возврата результата и причины несработки).
Уровни изоляции транзакции курсоров уточнены и проверены под нагрузкой на 4-х тестовых базах данных летом и осенью 2019-го года.

Для обхода попадания на вложенную обработку исключений на клиентах:
 - установить или обновить **Драйвер ODBC для MS SQL** (дистрибутив версии 17 и руководство см. на сервере в папке `Q:\M$_Windows\SQL_Server\Driver ODBC for SQL Server`),
 - поднять **Системный DSN** в источниках данных ODBC (см. `Подключение к БД через системный DSN` на сервере в папке проекта `..\SQL & XML (XPath & XQuery XSD XDR XSLT)`).

Контроль подключения и его восстановление при разрыве (например, при плохом контакте на коннекторах, через Wi-Fi или через мобильный Интернет) не предусматривается.

Выпуск релизов и пакетов не предусматривается. так как программное обеспечение на распространяется. 

#### История изменений и улучшений в базах данных

Версия 3 (устарела):
 - с ошибками в загрузке данных (исправили в версии 4, 5),
 - оставили как образец наработок и для анализа.

Версии 4, 5 (устарела):
 - 5-ая версия для проверки правильности загрузки данных для 4-ой,
 - добавили обход взаимоблокировок на нарастающих временных задержках,
 - у летательных аппаратов регистрация и авиакомпании не указываются,
 - авиарейсы плюсуются без даты,
 
Версия 6 (текущая):
 - авиарейсы вставляются по датам,
 - у летательных аппаратов обновляется регистрация и авиакомпания-оператор крайнего авиарейса (исправлено в версиях 7 и 8),
 - удачно проиндексировали поля (загрузка ускорилась в 25 ... 35 раз, простои на взаимоблокировках уменьшились),
 
Версия 7 (в процессе разработки, пока на паузе, наработки переносятся в версию 8):
 - у летательных аппаратов по принципу _медленно меняющейся размерности_сделана хронология регистраций
   (бизнес-ключ - сочетание заводских номеров, суррогатный ключ - регистрации по периодам использования соответственно),
 - а также сделана хронология авиакомпании-оператора, авиакомпании-владельца, авиакомпании-арендатора, авиакомпании-лизингодателя
   (бизнес-ключ - тот же, суррогатные ключи - авиакомпании по периодам использования соответственно) через отдельные справочные таблицы, 

Версия 8 (в процессе разработки):
 - хронология регистраций и тех же авиакомпаний пишется в XML-ных полях,
 - убрали отдельную базу данных по летательным аппаратам,
 - добавили отношения, индексы, XSD-схемы, каскадные правила на удаления и обновления.

#### Доработки.

Сделать графическую формочку для правки свойств альянсов (или делать это внутри Management Studio). Добавить ссылку на каждый в Wikipedia.

Сделать графическую формочку для правки свойств летательных аппаратов и уточнить набор виджетов на ней,
ссылаться на их фото на https://www.jetphotos.com (присутствуют немодерирруемые несоответствия).

Добавить на графической формочке свойств объектов поиск по названию объекта в выпадающем списке с автодополнением из уже имеющихся названий объектов в базе данных,
добавить виджеты на вкладке ВПП (широта, долгота, абсолютная отметка, длина, ширина, покрытие полос, оснащение системой сближения и посадки и т. д.),
ссылку по объекту на статью в Wikipedia.

Для подписания и утверждения внесения изменений в справочные данные предусмотреть использование **сертификата (ЭЦП)** на USB-ом токене. Предусмотреть возможность вывода истории внесения изменений с указанием подписантов. Требуются **DDK** или **SDK** от фирмы-изготовителя USB-вых токенов для добавления диалога открытия содержимого токена и выбора на нем требуемого сертификата в пользовательском режиме.

На сайте (см. (*) выше) показать маршруты в виде их профилей на топологии с привязкой к карте на https://www.google.com/maps , опираясь на аналитику баз данных.

Доработать асинхронную загрузку оперативных данных на API-шках по ВЭБ-хукам с http://www.flightradar24.com и с первичного оборудования.

Проанализировать базы данных с целью дальнейшего улучшения ее производительности с нескольких клиентов в локальной подсети.
 
Остальные замечания см. в исходниках по тэгам **todo** и **fixme**
