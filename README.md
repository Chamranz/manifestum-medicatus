2# Manifestum Medicatus

*(от лат. «манифестовое волшебство»)*

Библиотека для генерации и валидации YAML-манифестов деплоя агентов (AEF) на основе
централизованного, слоистого хранилища параметров. Вместо того чтобы вручную держать
по 4 манифеста × 7 стендов на каждого агента, вы один раз описываете, что у агентов
общее и что различается, а дальше манифесты для всех стендов и всех агентов генерятся
автоматически и проходят валидацию через Pydantic-модели.

## 1. Идея

Манифесты собираются из трёх осей:

1. **Тип манифеста** — `agents`, `common`, `namespace`, `integrations`. Каждому
   соответствует своя Pydantic-модель в [`manifestum_medicatus/models/`](manifestum_medicatus/models/).
2. **Scope** — `all` (общее для всех агентов, живущих в одном AEF-контейнере) или
   конкретный агент (например, `document_classifier`). Всё, что есть в `scope=all`,
   подмешивается первым; агентский слой поверх него может что-то переопределить.
3. **Слой стенда** — иерархия наследования, задана в
   [`cli/main.py:STAND_LAYERS`](manifestum_medicatus/cli/main.py):

   ```
   DEV   = general → PREPROM         → DEV
   IFT1  = general → PREPROM → IFT   → IFT1
   IFT2  = general → PREPROM → IFT   → IFT2
   PROM1 = general → PROM            → PROM1
   PROM2 = general → PROM            → PROM2
   PSI1  = general → PSI             → PSI1
   PSI2  = general → PSI             → PSI2
   ```

   Каждый следующий слой в цепочке переопределяет предыдущий (deep merge; списки вида
   `MTLS`/`KAFKA.CLUSTERS`/`INGRESS_WHITELIST`/`POSTGRES` мерджатся по ключу `NAME`,
   но каждый элемент списка заменяется **целиком** — см. раздел «Особенность списков» ниже).

Физически это выглядит как дерево python-модулей:

```
manifests_diff/
  agents/
    all/
      general.py              # scope=all, слой general
      PREPROM/preprom.py       # scope=all, слой PREPROM
      ...
    document_classifier/
      general.py               # scope=document_classifier, слой general
      DEV/dev.py
      PREPROM/preprom.py
      IFT/ift.py
      IFT1/ift1.py
      ...
  common/
    all/general.py
    document_classifier/general.py   # пока не используется, см. «Известные ограничения»
  namespace/...
  integrations/...
```

Каждый файл слоя — это Python-модуль с функцией `get_config()`, возвращающей `dict`
(обычно через `SomeModel(...).model_dump(exclude_unset=True)` — важно именно
`exclude_unset`, иначе в дамп попадут все дефолты модели, включая служебные заглушки).
Слой опционален: если файла нет, он просто пропускается.

### Соглашение "Укажи меня"

Многие поля в моделях (`manifestum_medicatus/models/*.py`) имеют дефолт-заглушку
`"Укажи меня"` вместо `None`. Если поле нигде по цепочке слоёв не переопределено,
итоговая валидация (`_save_manifest`, без `exclude_unset`) честно положит эту строку
в финальный YAML — это осознанный сигнал «здесь нужно реальное значение, не забудь
проставить руками» до деплоя. Наличие `Укажи меня` в выхлопе — не баг, а to-do.

## 2. Установка

```bash
pip install -e .
```

Даёт консольную команду `manifestum` (см. `pyproject.toml:[project.scripts]`).
Без установки все команды ниже так же работают через `python -m manifestum_medicatus.cli.main`.

## 3. Команды

### 3.1. `generate` — сгенерировать YAML из manifests_diff

```bash
manifestum generate \
  --config-dir manifests_diff \
  --output-dir ./output \
  --agents cash_flow document_classifier \
  --stands DEV IFT1 IFT2 PROM1 PROM2 PSI1 PSI2
```

`--stands` и `--agents` не обязательны: без `--stands` берутся все 7, без `--agents`
автоматически определяются все существующие агенты в `manifests_diff` и генерация
происходит для каждого из них.

Результат — `output/<agent>/<manifest_type>/<STAND>.yaml`. Каждый агент получает
свою отдельную директорию, внутри которой лежат папки `agents/`, `common/`,
`integrations/`, `namespace/` с манифестами по стендам:

```
output/
├── cash_flow/
│   ├── agents/DEV.yaml
│   ├── agents/IFT1.yaml
│   ├── ...
│   ├── common/COMMON.yaml
│   ├── integrations/DEV.yaml
│   ├── namespace/DEV.yaml
│   └── ...
├── document_classifier/
│   └── ...
└── ...
```

### 3.2. `import-agent` — затащить уже готовые yaml в manifests_diff

Если у вас уже есть руками сведённые манифесты агента на все 7 стендов (как в папках
`cash-flow/`, `classifier/` в этом репозитории — исторические примеры), эта команда
разложит их по иерархии слоёв автоматически и вынесет в `scope=all` всё, что совпадает
у нескольких агентов на одинаковой позиции иерархии:

```bash
manifestum import-agent \
  --config-dir manifests_diff \
  --agent cash_flow=cash-flow \
  --agent document_classifier=classifier
```

Можно передать и одного агента — тогда всё его содержимое ляжет в его собственный
scope (сравнивать не с чем, выносить в `all` нечего). Добавление ещё одного агента
позже автоматически подхватит то общее, что появится между ним и уже импортированными.

Программный интерфейс — [`core/importer.py`](manifestum_medicatus/core/importer.py):
`bootstrap_agents()` (agents/namespace/integrations) и `bootstrap_common()` (common).

### 3.3. `onboard-agent` — завести нового агента с нуля

Для агента, у которого ещё нет ни одного готового манифеста — только КЭ модуля и имя:

```bash
manifestum onboard-agent \
  --config-dir manifests_diff \
  --agent-scope claim_terms \
  --agent-name claim-terms \
  --ci CI10071234
```

Команда читает `hub.id`/`aef.id` из уже заполненного `common/all/general.py` (то есть
онбординг нового агента возможен только после того, как в `manifests_diff` уже есть
хотя бы один агент — константы контейнера берутся оттуда) и создаёт минимальный слой
для нового агента:

- `agents/{scope}/general.py` — `AGENT_NAME`, `ENV.AGENT_ID`, `ENV.POD_NAMESPACE`,
  `ENV.TRACING_SERVICE_KAFKA_BOOTSTRAP_SERVERS`;
- `namespace/{scope}/general.py` — `DROPAPP_NAMESPACE`, `EIGW_NAMESPACE`;
- `namespace/{scope}/<STAND>/...` — `SECMAN.SBER_CA_SERVER_CN` на каждый физический
  стенд (нужен `DROPAPP_CLUSTER` этого стенда, который уже есть в `namespace/all`);
- `namespace/{scope}/<DEV|IFT|PROM|PSI>/...` — `SECMAN.SBER_CA_CLIENT_CN` на группу
  стендов одного типа.

Все остальные поля (RESOURCES/sizing, ISTIO/OTT/GEOROUTES, кастомные ENV-переменные,
свои Kafka-топики, запись в `common.agents[]`/`aef.module_id`) **сознательно не
генерируются** — неверная догадка тут хуже отсутствия значения. Это осознанные ручные
доработки после онбординга; там, где модель считает поле обязательным, оно само
всплывёт как `Укажи меня` в `generate`-выхлопе.

Программный интерфейс — [`core/onboarding.py`](manifestum_medicatus/core/onboarding.py):
`scaffold_agent()`.

## 4. Особенность списков при мердже

`deep_merge` ([`core/merger.py`](manifestum_medicatus/core/merger.py)) мерджит списки
вида `MTLS`, `KAFKA.CLUSTERS`, `INGRESS_WHITELIST`, `POSTGRES` по ключу `NAME`, но
**заменяет найденный элемент целиком**, а не мерджит поля внутри него. Поэтому:

- Инструменты импорта/онбординга (`importer.py`, `onboarding.py`) специально трактуют
  такие списки как атомарные значения при сравнении слоёв: либо весь список одинаков
  и выносится в `all` целиком, либо остаётся целиком в более специфичном слое.
- Если правите такие слои руками — не разбивайте один элемент списка на два слоя
  (например, `NAME`+`PORT` в одном файле, `HOST` в другом): второй слой при мердже
  затрёт первый целиком, а не дополнит его.

## 5. Известные ограничения

- **`common` не поддерживает agent-scope.** В генераторе (`cli/main.py:NO_AGENT_MANIFESTS`)
  `common` считается общим для всех агентов и сохраняется в единственный
  `output/common/COMMON.yaml`. По факту `aef.module_id` и список `agents[]` (git/путь/
  sonar-ключ/docker-образ) в `COMMON.yaml` различаются по агентам — сейчас эти поля
  просто не выносятся ни в `all`, ни в agent-scope и остаются `Укажи меня` /
  незаполненными после импорта или онбординга. Это осознанно отложено; когда дойдут
  руки чинить многоагентность `common`, нужно снять `common` из `NO_AGENT_MANIFESTS` и
  решить, как агрегировать `agents[]` нескольких агентов одного контейнера в одном файле.
- Онбординг нового агента не трогает `ISTIO`/`OTT`/`GEOROUTES` и `integrations` —
  это протокольные/бизнес-решения (нужен ли агенту OTT, свои Kafka-топики и т.п.),
  которые небезопасно угадывать по одному имени и КЭ.
