
/***
Get the update for the navbar 
***/
var currentChat = -1;

function getUpdate(){
  $.get("{% url 'get_updates_ajax' %}", function(messages){
      $("#requestC").html('');
      if(messages.requestC != 0 && !($("#reqModal").is(":visible")))
      {
        $("#requestC").append(messages.requestC)
      }

      $("#messageC").html('');
      if(messages.messageC != 0 && !($("#chatModal").is(":visible")))
      {
        $("#messageC").append(messages.messageC)
      }
      $("#regularC").html('');
      if(messages.regularC != 0)
      {
        $("#regularC").append(messages.regularC)
      }
  });
}


/***
Keep updating 
***/
var updateInterval = 2500
$(function(){
  getUpdate();
  refreshTimer = setInterval(getUpdate, updateInterval)
});




var $input = $('<div class="modal-body"><input type="text" class="form-control" placeholder="Message" id = "myMessage"></div>')
var $newMsgToInput = $('<div class="modal-body">To:  <input type="text" autocomplete = "off" class = "plain-text" id = "toMsg" onkeyup="return runScript(event)"></input></div>')
var $newMsgChatInput = $('<div class="modal-body"><input type="text" class="form-control" placeholder="Message" id = "myNewMessage" onkeyup = "createChat(event)"></input></div>')


$(document).on('click', '.js-newMsg', function () {
  $('.js-msgGroup, .js-newMsg').addClass('hide')
  $('.js-userSuggestion').removeClass('hide')
  $('.modal-title').html('<a href="#" class="js-gotoMsgs2">Back</a>')
  $newMsgToInput.insertBefore('.js-modalBody')
  $('#toMsg').focus()
})

$(document).on('click', '.js-msgGroup', function () {
  $('.js-msgGroup, .js-newMsg').addClass('hide')
  $('.js-conversation').removeClass('hide')
  $('.modal-title').html('<a href="#" class="js-gotoMsgs">Back</a>')
  $input.insertAfter('.js-modalBody')
  $('#myMessage').focus()
})


$(document).on('click', '.js-gotoMsgs2', function () {
  $newMsgToInput.remove()
  $newMsgChatInput.remove()
  $('.js-conversation, js-userSuggestion').addClass('hide')
  $('.js-msgGroup, .js-newMsg').removeClass('hide')
  $('.modal-title').html('Messages')
})

$(document).on('click', '.msgChat', function(event){
  currentChat = this.id;
  //updateChat()
})

function updateChat(){
  $.ajax({
      type: "POST",
      url: "{% url 'get_chat_ajax' %}",
      data: {
        csrfmiddlewaretoken: "{{ csrf_token }}",
        chatID: currentChat
      },
      success: function(data){
        // $("#msg_dropdown").html('');
        

        // $(data.notifications).each(function(){
        //   $("#msg_dropdown").append(this);
        // })

      },
      error: function(rs, e) {
        console.log(rs);
        console.log(e);
      }
    })
}


/***********
New Message
***********/

//The index of the user selection
var userSelection = 0
//The index of the last selection
var lastSelection = 0
//The length of the usersArray
var selectionLength = 0
//The array of choices
var usersArray = []
//The array of selected users
var selectedUser = []

var toNum = 0
function runScript(e) {
  var toUser = $('#toMsg')[0].value;
  
  if (e.keyCode == 13) {
  //enter
    if (usersArray.length != 0 && userSelection != -1 && userSelection < usersArray.length)
    {
      toNum += 1;
      $newBadge = $('<span class="badge" style = "background-color : #3097d1;" id = "to'+toNum+'">' + usersArray[userSelection] + '</span>')
      $newBadge.insertBefore('#toMsg')
      selectedUser.push(usersArray[userSelection])

      $('#toMsg').val('');
      $newMsgChatInput.insertAfter('.js-modalBody')
      $("#userSuggestion").html('');
    }
  }else if(e.keyCode == 38){ 
  //arrow up
    lastSelection = userSelection
    if(userSelection < 0)
    {
      userSelection = selectionLength - 1;
    }else{
      userSelection -= 1
    }
    selectNewUser()
  }else if (e.keyCode == 40){ 
  //arrow down
    lastSelection = userSelection
    if(userSelection >= selectionLength)
    {
      userSelection = 0;
    }else{
      userSelection += 1
    }
    selectNewUser()
  }
  else if(event.keyCode == 8 && toUser == '')
  // backspace
  {
    $("#userSuggestion").html('');

    var $lastBadge = document.getElementById("to"+toNum);
    if(toNum != 0)
    {  
      $lastBadge.remove()
      selectedUser.pop()
      toNum -= 1;
      if(toNum == 0)
      {
        $newMsgChatInput.remove()
      }
    }
  }else if(toUser != '')
  //get the suggestion down
  {
    $.ajax({
      type: "POST",
      url: "{% url 'get_user_suggestion_ajax' %}",
      data: {
        csrfmiddlewaretoken: "{{ csrf_token }}",
        'selected[]': selectedUser,
        slug: toUser
      },
      success: function(data){
        $("#userSuggestion").html('')

        selectionLength = 0

        $(data.suggestions).each(function(){
          $("#userSuggestion").append(this)
          selectionLength += 1
        })

        userSelection = 0
        usersArray = data.users
        selectNewUser()

      },
      error: function(rs, e) {
        console.log(rs);
        console.log(e);
      }
    })
  }else{
  //
    $("#userSuggestion").html('')
  }
}

/****
This function is called after pressing enter in new message menu
*****/
function createChat(e){
  if(e.keyCode == 13){
    /* create new chat here */
    var newMessage = $("#myNewMessage")[0].value;
    
    $("#myNewMessage").val('')
    
    $.ajax({
      type: "POST",
      url: "{% url 'create_chat' %}",
      data:{
        csrfmiddlewaretoken: "{{ csrf_token }}",
        'selected[]': selectedUser,
        'message': newMessage
      },
      success: function(data){
  

      },
      error: function(rs, e) {
        console.log(rs);
        console.log(e);
      }
    })
  }
}

//selecting a new user while creating a new chat
function selectNewUser(){
  var lastTag = "#user" + lastSelection
  $(lastTag).css("background-color", "white")

  var myTag = "#user" + userSelection
  $(myTag).css("background-color", "gray")
}

//navbar
$(document).ready(function(){
  //Ajax function for the request button
  $("#request-toggle").click(function(e){
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: "{% url 'get_requests_ajax' %}",
      data: {
        csrfmiddlewaretoken: "{{ csrf_token }}"
      },
      success: function(data){
        $("#notification_dropdown").html('');
        

        $(data.notifications).each(function(){
          $("#notification_dropdown").append(this);
        })

      },
      error: function(rs, e) {
        console.log(rs);
        console.log(e);
      }
    })
  })

  //Ajax function for the message button
  $("#msg-toggle").click(function(e){
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: "{% url 'get_messages_ajax' %}",
      data: {
        csrfmiddlewaretoken: "{{ csrf_token }}"
      },
      success: function(data){
        $("#msg_dropdown").html('');
        

        $(data.notifications).each(function(){
          $("#msg_dropdown").append(this);
        })

      },
      error: function(rs, e) {
        console.log(rs);
        console.log(e);
      }
    })
  })

})