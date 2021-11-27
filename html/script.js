var socket;
var usernameInput
var chatIDInput;
var messageInput;
var chatRoom;
var dingSound;
var messages = [];
var delay = true;
var sent = [];
var sentOn = 0;

function onload(){
  socket = io();
  usernameInput = document.getElementById("NameInput");
  chatIDInput = document.getElementById("IDInput");
  messageInput = document.getElementById("ComposedMessage");
  chatRoom = document.getElementById("RoomID");
  dingSound = document.getElementById("Ding");

  socket.on("join", function(room){
    chatRoom.innerHTML = "Chatroom : " + room;
  })

  socket.on("recieve", function(message){
    console.log(message);
    splitM = message.split(";");
    message = "~~~~~:" + splitM[1];
    splitD = splitM[1].split("|");
    if(splitD[0] == "IMAGE"){
      document.getElementById("image").src ="data:image/jpeg;charset=utf-8;base64," + splitD[1];
    }
    else{
    if (messages.length < 9){
      messages.push(message);
      dingSound.currentTime = 0;
      dingSound.play();
    }
    else{
      messages.shift();
      messages.push(message);
    }
    }
    for (i = 0; i < messages.length; i++){
        document.getElementById("Message"+i).innerHTML = messages[i];
        document.getElementById("Message"+i).style.color = "#303030";
    }
  })
}

function Connect(){
  socket.emit("join", chatIDInput.value, usernameInput.value);
}

function Send(){
  sentOn = 0;
  sent.unshift(messageInput.value);
  if (delay && messageInput.value.replace(/\s/g, "") != ""){
    delay = false;
    setTimeout(delayReset, 1000);
    socket.emit("send", messageInput.value);
    messageInput.value = "";
  }
}

function delayReset(){
  delay = true;
}

function onKeyDown(e){
  if(e.keyCode == 13){
    document.getElementById("SendMessage").click();
    
  }
  else if(e.keyCode == 38){
    sentOn++;
    if(sentOn == 1  && sent[0] != messageInput.value){
    sent.unshift(messageInput.value);
    }
    if(sentOn > sent.length - 1){
      sendOn = sent.length;
    }
    messageInput.value = sent[sentOn];
    console.log(sent)
  }
  else if(e.keyCode == 40){
    sentOn--;
    if(sentOn < 0){
      sentOn=0;
    }
    messageInput.value = sent[sentOn];
  }
}
document.addEventListener("keydown", onKeyDown)