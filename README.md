# LoadWorkDataAirFlightsDBNew

#### Общее описание
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
 - (*) Сайт разрабатывается отдельно и в объем данного проекта не входит.

###### Хранение информации в файлах различных типов и их использование `[Рисунок 2]`

![1 001 001](https://user-images.githubusercontent.com/104857185/167037090-9cd548c0-9643-4903-adce-13e2a039226d.jpg)
_Файлы, открываемые только в своем ПО, желательно не использовать_

----
Предусматривается:
 - разработка баз данных и администрирование сервера СУБД с помощью **Management Studio (SSMS)**,
 - работа клиентов на графических формах (в части UX/UI) в локальной подсети или через RDP из внешней сети по учеткам Windows Server-ов без контроллера домена с заранее заданной конфигурацией сервера СУБД (имена входа, их права) и с ПО в оригинале на файловом сервере, которое дорабатывается в процессе (в части CI/CD) без уведомления клиентов.

###### Отчеты по базам данных из Management Studio

![СУБД Полная - Простая - Сжатие - Полная 001 002](https://user-images.githubusercontent.com/37275122/168450352-48a1e7e1-eeb4-4227-b744-2d368fccac32.png)

![СУБД Полная - Простая - Сжатие - Полная 001 003](https://user-images.githubusercontent.com/37275122/168450358-630fa494-2c0f-4bad-afb1-42bdb44325ec.png)

![СУБД Полная - Простая - Сжатие - Полная 001 004](https://user-images.githubusercontent.com/37275122/168450362-8de3b141-e670-4067-a28e-544cd9cff239.png)

![СУБД Полная - Простая - Сжатие - Полная 001 005](https://user-images.githubusercontent.com/37275122/168890832-25179657-69dd-47e9-8bac-63e5ac56715e.png)

----
Для обхода попадания на вложенную обработку исключений на клиентах:
 - при необходимости установить или обновить **двайвер ODBC для MS SQL** (дистрибутив версии 17 и руководство см. на сервере в папке `Q:\M$_Windows\SQL_Server\Driver ODBC for SQL Server`),
 - в источниках данных ODBC поднять **Системный DSN** (см. "Подключение к БД через системный DSN" на сервере в папке проекта `..\Руководства в картинках`).
 
Уход от взаимоблокировок при загрузке рабочих и оперативных данных с нескольких внешних клиентов на сервер СУБД выполняется обертыванием тела цикла попыток с нарастающей задержкой по времени в обработку исключения, так как сервер СУБД не дает обратные вызовы (хуки или программные прерывания) клиентам на повторную попытку, если запрашиваемые данные пока заняты. Без обратных вызовов пока не получается эффективно задействовать внешний сервер СУБД. Транзакции сделаны короткими, но между ними все перезапрашивается снова, так как данные изменяются другими клиентами. Потери времени на задержках частично уменьшены путем уточнения уровня изоляции транзакции в зависимости от действия. Число перезапросов и их перенос по времени пишутся в журнал загрузки рабочих данных (см. `LogReport_DBNew6.txt` в папке проекта на сервере, `ErrorLog.txt` там же - ошибки дозаписи в него). Начальное значение задержки по времени и шаг ее приращения подобран экспериментально по результатам нагрузочных тестов осенью 2019-го года и зависит от вычислительных характеристик сервера СУБД. При 2-х кратном увеличении количества клиентов задержки увеличиваются на 15 ... 20 %, а нагрузка на сервер СУБД (процессор, HDD) уменьшается на 25 ... 35 % благодаря удачно проиндексированным полям в таблицах. Пропускная способность локальной подсети достаточная.

Каждый клиент использует непрерывное подключение с несколькими клиентскими статическими однопроходными непрокручиваемыми API-курсорами ODBC. При вызове хранимой процедуры используются серверные курсоры. Но хранимые процедуры применяются мало, потому что по мере усложнения прикладного функционала выполнить его только средствами SQL сложно (бедность типов данных и синтаксиса, сложность передачи и возврата составных типов данных, пока нет способа возврата результата и причины несработки). Уровни изоляции транзакции курсоров уточнены и проверены под нагрузкой на 4-х тестовых базах данных летом и осенью 2019-го года.

Контроль подключения и его восстановление при разрыве (например, при плохом контакте на коннекторах, через Wi-Fi или через мобильный Интернет) не предусматривается.

Модель восстановления баз данных - **ПОЛНАЯ**, так как в хранимых процедурах используются помеченные транзакции. Обслуживание баз данных (целостность, индексы, бэкапы) делается обычным способом - на время все действия завершаются до уведомления о возобновлении работы.

Загрузка рабочих и оперативных данных выполняется в отдельном потоке и не требует соответствия хронологии.

----
#### Объемы доработок:

Уточнить использование комплектного с **MS SQL** функционала **XPath & XQuery** и комплектной спецификации **SQL/XML**, чтобы парсить поля **XML(CONTENT dbo.XSD-схема)** как **DOM** в базе данных летательных аппаратов и писать в нее XML-ное поле с регистрацией и по одному XML-ному полю на лизингодателя, арендодателя, арендатора (владельца) и оператора при их наличии для каждого авиарейса следующим образом:
 - В каждом XML-ном поле у одной авиакомпании может быть только одна ветка с **аттрибутом-идентификатором**, указывающим на соответствующую запись в базе данных авиакомпаний (далее по тексту аттрибутом).
 - В некоторых XML-ных полях может быть еще одна ветка с аттрибутом пустой авиакомпании. Например, когда на одном авиарейсе владелец и оператор - одна и та же авиакомпания (нет лизинга, нет аренды, нет оператора). На другом авиарейсе - одна - владелец, вторая - оператор (нет лизингодателя и нет арендодателя). На следующем авиарейсе одна - арендодатель, вторая - арендатор, третья - оператор (нет лизингодателя). И т. д. в разных сочетаниях.
 - Или в разных XML-ных полях авиакомпаний аттрибут ветки может ссылаться на одну авиакомпанию.
 - В каждой ветке может быть одна или несколько подветок с датами по количеству периодов использования (начало временного диапазона) в данной авиакомпании.
 - В соответствии с этим при необходимости пишем новую ветку и подветку или дописываем в существующую ветку новую подветку в соответствии с хронологией.
 - А также убираем предыдущие подветки, если они остаются не в начале временного диапазона в данной авиакомпании.
 - Считаем, что начало временного диапазона в следующей авиакомпании совпадает с окончанием временного диапазона использования в предыдущей, в том числе пустой.
 - Для XML-ного поля регистрации аналогично.

###### Делаем **XML**-ное поле

![Таблица с полем типа xml с привязкой к схеме xsd](https://user-images.githubusercontent.com/104857185/167261417-e0820f3d-965f-4124-9af6-e59994e09f46.png)

 - Для облегчения отладки выносим запись или обновление каждого XML-ного поля в хранимую процедуру вместе с частью на XPath & XQuery.
 - Считаем, что любая авиакомпания может быть лизингодателем, арендодателем, владельцем или оператором, поэтому все их XML-ные поля в хранимой процедуре пропускаем через одну XSD-схему (каждое XML-ное поле через свой элемент XSD-схемы в соответствии с его именем) за один раз.

###### Делаем схему на все **XML**-ные поля и привязываем ее к ручному вводу данных в **XML** 

![SSMS - XML-код - Создать схему](https://user-images.githubusercontent.com/104857185/167261451-a42a0c66-2888-4042-88a2-679f1ef6549a.png)

_Поправка по терминологии:
То, что в Management Studio называется **коллекцией схем XML**, точнее называть XSD-схемой. Понимает только файл *.xsd. В одной XSD-схеме несколько элементов со своими именами. Пространство имен одно на все элементы XSD-схемы (см. https://www.w3schools.com/xml/schema_simple.asp и https://www.w3.org/TR/xmlschema11-1/). Генерируется из XML внутри Management Studio или с помощью файла *.xslt. Добавляется скриптом._
 
Недостаток хранимой процедуры - не возвращает в скрипты на Python-е результат своей работы (получилось, не получилось с указанием причины). Недостаток XSD-схемы - тот же и тот, что она пропускает все или не пропускает ничего. Делаем как обычно, просто фиксируем и записываем отказ этого действия в журнал для анализа. 
 
Дополнить структуру базы данных по авиакомпаниям (история, владельцы и остальное). Соответственно выбрать способ работы с ними для клиентов. Добавить ссылку на нее с Wikipedia.

Сделать графическую формочку для правки свойств альянсов (или делать это внутри Management Studio). Добавить ссылку с Wikipedia.

Сделать графическую формочку для правки свойств летательных аппаратов и уточнить набор виджетов на ней, в том числе их фото (выделить таблицы с мультимедийными полями в отдельную файловую группу, которую вынести на дисковую полку "холодного хранения") или ссылаться на их фото на https://www.jetphotos.com (присутствуют немодерирруемые несоответствия).

Добавить на графической формочке свойств объектов поиск объекта по названию в базе данных с выпадающим списком с автодополнением.

Добавить на графической формочке для правки свойств объектов виджеты на вкладке ВПП (широта, долгота, абс. отметка, длина, ширина, покрытие полос, оснащение системой сближения и посадки и т. д.), ссылку по объекту на Wikipedia, поиск по наименованию в виде выпадающего списка (требуется интеграция с поиском Google-а).

Добавить возможность разрешения на внесение изменений в базы данных исполнителями через удостоверение пользователей **сертификатом (ЭЦП)** на USB-ом токене, а также подписание извещения на внесение изменений перед их внесением главным специалистом **сертификатом (ЭЦП)** на USB-ом токене. Предусмотреть возможность вывода истории внесения изменений с указанием подписантов (требуются **DDK** или **SDK** от фирмы-изготовителя USB-вых токенов для добавления диалога открытия содержимого токена и выбора на нем требуемого сертификата в пользовательском режиме).

Дополнить данные по маршрутам их профилями и топологиями с привязкой к картам Google, а также их изменениями с течением времени.

Разработать асинхронную загрузку оперативных данных на API-шках по ВЭБ-хукам с http://www.flightradar24.com и с первичного оборудования.

Выполнить визуализацию части данных на ВЭБ-сайте ВЭБ-сервера в этой же локальной подсети.

Проанализировать базы данных с целью дальнейшего улучшения ее производительности с нескольких клиентов в локальной подсети.
 
----
Остальные замечания см. в исходниках по тэгам **todo** и **fixme**
