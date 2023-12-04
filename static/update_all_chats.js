function updateChatsList() {
    $.ajax({
        url:  '/chat/updated-chats-data/',  // URL вашего AJAX представления
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            $('#chats-list .chats-menu-container').empty();
            // Проходим по каждому объекту в массиве и создаем HTML-разметку
            data.chats_list.forEach(function(chat) {
                var chatMenuBar = $('<div class="chat-menu-bar"></div>');
                var link = $('<a></a>').attr('href', chat.link).html(chat.user.full_name);

                chatMenuBar.append(link);

                if (chat.count_unread > 0) {
                    var countUnread = $('<span style="float: right;"></span>').text(chat.count_unread);
                    chatMenuBar.append(countUnread);
                }

                $('#chats-list .chats-menu-container').append(chatMenuBar);
            });
        },
        complete: function() {
            setTimeout(updateChatsList, 1000); // Повторите обновление каждые 2 секунды
        }
    });
}

$(document).ready(function() {
    updateChatsList(); // Начните обновление данных при загрузке страницы
});

