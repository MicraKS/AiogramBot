## Win a password from a bot

### Концепция

Бот, который выдает пароль пользователю после того, как пользователь обиграет его в крестики нолики.
Пароль выдается в соответствии с успехами пользователя против бота.

Например, если пользователь проиграет боту несколько раз подряд, то бот выдаст ему легкий пароль, по типу qwerty.
Если пользователь обыграл бота с первого раза, тогда бот выдаст сложный символьный пароль.

### Техническая документация

#### Сценарий старта
- После первого добавления бота и нажатии кнопки старта или ввода команды `/start` бот выдает пользователю инлайн клавиатуру с описанием и полем со случайной игрой.

#### Сценарий игры в крестики нолики
 - В описании указано, что пользователь может попытать удачу с ботом, сыграв с ним в игру, а наградой будет пароль.
 - Поле для игры в крестики нолики 3х3 по дефолту заполнено ⬜️
 - Первый ход делает пользователь, когда он нажимает на любую клетку, она превращается в ❌
 - После этого, спустя 1000ms свой ход делает бот и ставит ⭕️ на любую другую клетку.
 - Пока ходит бот, пользователю блокируется взаимодействие с игровым полем
 - Тот кто первый соберет 3 крестика или нолика в ряд по вертикали, горизонтали и диагонали - тот и выигрывает.
 - Если выиграл бот, то описание клавиатуры меняется рандомно на фразу из списка проигрышей, например - "Очередная победа искусственного интеллекта над кожаными мешками. Можете попробовать еще раз :3"
 - Количество проигрышей записывается в базу данных.
 - Если выиграл человек, то бот рандомно берет фразу из списка выигрышей и выдает пользователю пароль.
 - Фраз в списке проигрышей и в списке выигрышей должно быть не менее 5, для каждого списка.
 - Пароль, который будет выдан пользователю, будет иметь корреляцию с количеством проигрышей. Чем выше количество проигрышей - тем легче будет пароль.