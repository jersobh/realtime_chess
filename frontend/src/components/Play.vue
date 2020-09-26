<template>
  <div id="game">
    <div id="board" >
    <div id="table" >
    <span v-if="player.role == 'watcher'">You've joined as watcher</span>
    <p v-if="positionInfo && positionInfo.turn !== player.role">Now it's <span style="color">{{positionInfo.turn}}'s </span> turn</p>
    <p v-if="positionInfo && positionInfo.turn == player.role">It's <span style="color: #FF0000;">your</span> turn</p>
    <chessboard class="chessboard" v-if="player.role == 'white'" @onMove="showInfo" :fen="currentFen" :onPromotion="promote"></chessboard>
    <chessboard class="chessboard" v-if="player.role == 'black'" orientation="black" @onMove="showInfo" :fen="currentFen" :onPromotion="promote"  ></chessboard>
    <chessboard class="chessboard" style="pointer-events: none;" v-if="player.role == 'watcher'" :fen="currentFen" ></chessboard>
    </div>
    <div id="chat-box" v-if="player.role !== 'watcher'">
    <textarea class="msg_area" v-model="msg" rows="4" cols="30" placeholder="Digite a mensagem"></textarea><br /><button class="btn" @click="sendMessage()">Send</button>
    </div>
    <div class="message-board" style="max-height:100px; overflow-y:scroll;">
      <div v-for="message in messages" :key="message.player">
        <span v-if="message.type == 'player_message' && message.player == player.id" class="me">
        {{message.time}}: {{message.msg}}
        </span>
      <span v-if="message.type == 'player_message' && message.player !== player.id" class="remote">
      {{message.time}}: {{message.msg}}
      </span>
      <span v-if="message.type == 'sys_message'" class="sys_message">
      {{message.msg}}
      </span>
      <br /><br />
      </div>
    </div>
    </div>

  </div>
</template>

<script>
import {chessboard} from 'vue-chessboard'
import 'vue-chessboard/dist/vue-chessboard.css'
import SockJS from 'sockjs-client'
export default {
  name: 'app',
  components: {
    chessboard
  },
  data () {
    return {
      currentFen: '',
      positionInfo: null,
      player: 'white',
      username: '',
      msg: '',
      messages: [],
      socket: null,
      ws_server: '/ws'
    }
  },
  methods: {
    sendMessage () {
      let self = this
      if (self.msg.length == '') {
        return false
      }

      var d = new Date();


      self.socket.send(
        JSON.stringify({
          type: "new_message",
          player_id: self.player.id,
          room: self.room,
          msg: self.msg,
          time: d.toLocaleTimeString()
        })
      );
      this.msg = ''
    },
    showInfo(data) {
        let self = this
        if(self.socket) {
          self.socket.send(JSON.stringify({'type': 'new_move', 'player': self.player.role, 'room': self.room, 'fen': data.fen}))
        }

        this.positionInfo = data
        if(self.positionInfo.turn == self.player.role) {
               document.getElementById("table").style.pointerEvents = "auto";
          } else {
               document.getElementById("table").style.pointerEvents = "none";
          }

    },
    resetGame() {
    if (confirm("Want to reset the game?") ) {
        this.currentFen = ''
      } else {
        return false
      }


    },
    promote() {
      if (confirm("Want to promote to rook? Queen by default") ) {
        return 'r'
      } else {
        return 'q'
      }
    }
  },
  created() {
    this.room = this.$route.params.room_name
  },
  mounted () {
     let self = this
     this.socket = new SockJS(this.ws_server, 'websocket', {debug: true});
     this.socket.onopen = function() {
          setInterval(function() { self.socket.send(
            JSON.stringify({
              type: "keepalive",
            })
          );
        },3000);
          self.socket.send(
            JSON.stringify({
              type: "new_player",
              room: self.room
            })
          );
     };

     self.socket.onmessage = function(e) {
         let msg_obj;
          if (typeof e.data == 'string') {
            msg_obj = JSON.parse(e.data)
          } else {
            msg_obj = e.data
          }
         if(msg_obj.type == 'set_player'){
           self.player = msg_obj
        }
        if(msg_obj.type == 'update'){
         self.currentFen = msg_obj.fen
       }

       if(msg_obj.type == 'sys_message'){
         self.messages.unshift({'type': 'sys_message', 'msg': msg_obj.text })
       }

       if(msg_obj.type == 'message'){
         self.messages.unshift({ 'type': 'player_message', 'player': msg_obj.player_id, 'time': msg_obj.time, 'msg': msg_obj.text })
       }
         //self.socket.close();
     };

     self.socket.onclose = function() {
         self.socket = new SockJS(this.ws_server, 'websocket', {debug: true});
     };

  }
}
</script>
<style>

  #board {
width: 80%;
margin: auto;
  }

#chat-box {
  height: 15%;
min-width: 30%;
margin: auto;
float: left;
}
.message-board {
  border: 1px solid #03A9F4;

  position: relative;
  max-height: 200px;
  overflow-y: scroll;
  padding: 2%;
  height: 15%;
  width: auto;
  margin: auto;
  min-width: 60%;
  float: left;
}
.msg_area {
width: 96%;
margin: auto;
border: 1px solid #03A9F4;
  background: #fff;
  color:#333;
}

.me {
  background: #03A9F4;
  color: #fff;
  float:right;
  right:0;
  padding:2px;
  padding-left: 8px;
  padding-right: 8px;
  border-radius: 4px;
}

.remote {
  background: #009688;
  left:0;
  color: #fff;
  float:left;
  padding:2px;
  padding-left: 8px;
  padding-right: 8px;
  border-radius: 4px;
}

.sys_message {
  color:red;
  margin: auto;
  width: 100%;

}

.chessboard {
  width: 320px;
  height: 340px;
  margin: 0 auto;
}

@media only screen and (max-width: 800px) {
  #chat-box {
    height: 15%;
  width: 98%;
  margin: auto;
  float: left;
  }

  .message-board {
    position: relative;
    max-height: 200px;
    overflow-y: scroll;
    padding: 2%;
    height: 15%;
    width: 100%;
    margin: auto;
    min-width: 50%;
    float: left;
  }
}
</style>
