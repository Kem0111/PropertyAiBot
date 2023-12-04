var chatInterval;

// Функция для обновления блока с сообщениями
function updateChat(chatId) {
    $.ajax({
        url: `/chat/${chatId}/get-updated-data/`,
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            // Перебираем полученные сообщения и добавляем их в контейнер
            if (data && Array.isArray(data.messages_list) && data.messages_list.length > 0) {
                $.each(data.messages_list, function(index, message) {
                    var senderClass = message.sender === 'user' ? 'user-message' : 'other-message';
                    var messageDiv = `<div class="message ${senderClass}">`;
                    messageDiv += '<a href="' + message.chat.user.url + '">' + message.chat.user.full_name + '</a>';
                    messageDiv += '<span> (new) </span>'
                    messageDiv += '<p>' + message.text + '</p>';
                    messageDiv += '</div>';
                    $('#message-container').append(messageDiv);
                });
               // Прокручиваем контейнер вниз после добавления новых сообщений
                var messageContainer = $('#message-container');
                messageContainer.scrollTop(messageContainer.prop("scrollHeight"));
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log("Status: " + textStatus);
            console.log("Error: " + errorThrown);
        }
    });
}

// Запускаем функцию обновления каждые 5 секунд
console.log('Update function is running')
setInterval(function() {
   var chatId = window.location.pathname.split('/').filter(Boolean).pop();
   updateChat(chatId);
}, 1000);
