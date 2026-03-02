## Task3

Реализованы построение инвернтированного индекса и булевый поиск.

### Как запускать

- Чтобы построить(обновить) инвертированный индекс нужно вызвать с командой `index_build` и передать путь к папке с
  файлами с токенами
  > ```shell
   >python python main.py index_build --tokens_folder ../Task2/Task2Results --output_filepath Task3Results/inverted_index.json
   >```
- Чтобы запустить и использовать булевый поиск нужно вызвать с командой `search` и передать путь к файлу с
  инвертированным индексом
  > ```shell
    > python main.py search --index_file Task3Results/inverted_index.json
    >```