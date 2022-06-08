
(function() {
    var $ChatInput;
  
    $ChatInput = $('.ChatInput-input');
  
    $ChatInput.keyup(function(e) {
      var $this, newText;
      if (e.shiftKey && e.which === 13) {
        e.preventDefault();
        return false;
      }
      $this = $(this);
      //if Enter is pressed then carryu out funcion
      if (e.which === 13) {
        console.log("Enter was clicked");
        var contenteditable = document.querySelector('[contenteditable]'),
        newText = contenteditable.textContent;
        console.log(contenteditable);
        var userHtml = '<div class="ChatItem ChatItem--customer"> <div class="ChatItem-meta"> <div class="ChatItem-avatar"> <img class="ChatItem-avatarImage" src="https://randomuser.me/api/portraits/women/0.jpg"> </div> </div> <div class="ChatItem-chatContent"> <div class="ChatItem-chatText">' + newText + '</div> <div class="ChatItem-timeStamp"><strong>Me</strong> · Today 05:49</div> </div> </div>';
       console.log(userHtml);
        $this.html('');
        $('#ChatWindow').append(userHtml);
        botResponse(newText);
        return $('#ChatWindow').animate({
          scrollTop: $('#ChatWindow').prop("scrollHeight")
        }, 500);
      }
    });
  
  }).call(this);

function addMessage(msg){
  var botHTML = '<div class="ChatItem ChatItem--expert"><div class="ChatItem-meta"><div class="ChatItem-avatar"><img class="ChatItem-avatarImage" src="https://randomuser.me/api/portraits/women/0.jpg"></div></div><div class="ChatItem-chatContent"><div class="ChatItem-chatText">'+msg+"</div></div></div>"
  $('#ChatWindow').append(botHTML);
}
//Send request user input to server to be handled
function botResponse(newText){
  $.ajax({
    type: "POST",
    url: "/postmethod",
    data: JSON.stringify(newText),
    contentType: "application/json",
    dataType: 'json',
    success: function(data){
        console.log(data);
        addMessage(data)
    }
});
}
  