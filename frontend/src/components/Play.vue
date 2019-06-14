<template>
  <div id="game">
    <div id="board" >
    <div id="table" >
    <span v-if="player.role">You've joined as {{player.role}}</span><br />
    <p v-if="positionInfo && positionInfo.turn !== player.role">Now it's <span style="color">{{positionInfo.turn}}'s </span> turn</p>
    <p v-if="positionInfo && positionInfo.turn == player.role">It's <span style="color: #FF0000;">your</span> turn</p>
    <chessboard v-if="player.role == 'white'" @onMove="showInfo" :fen="currentFen" :onPromotion="promote"></chessboard>
    <chessboard v-if="player.role == 'black'" orientation="black" @onMove="showInfo" :fen="currentFen" :onPromotion="promote"  ></chessboard>
    <chessboard v-if="player.role == 'watcher'" :fen="currentFen" style="pointer-events: none"></chessboard>
    </div>
    <textarea class="msg_area" v-model="msg" rows="4" cols="30"></textarea><br /><button class="btn" @click="sendMessage()">Send</button>
    <div class="message-board" style="max-height:100px; overflow-y:scroll;">
      <div v-for="message in messages" track-by="id">
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
  watch: {
    currentFen: function (newVal, oldVal) {
      let self = this
      console.log('new move')
      console.log(self.positionInfo)

// To re-enable:

    }
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
        console.log(self.positionInfo)
        if(self.positionInfo.turn == self.player.role) {
            console.log('enable click')
               document.getElementById("table").style.pointerEvents = "auto";
          } else {
            console.log('disable click')
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
     console.log('connected');
          var t=setInterval(function() { self.socket.send(
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
          console.log('ao')
          console.log(e.data)
          console.log(typeof e.data)
          if (typeof e.data == 'string') {
            msg_obj = JSON.parse(e.data)
          } else {
            msg_obj = e.data
          }
         console.log(msg_obj.type)
         //let obj = JSON.parse(e.data)
         if(msg_obj.type == 'set_player'){
           console.log('setting color')
           self.player = msg_obj
           console.log(self.player)
        }
        if(msg_obj.type == 'update'){
          console.log('new move')
         self.currentFen = msg_obj.fen
       }

       if(msg_obj.type == 'sys_message'){
         console.log('new sys message')
         self.messages.unshift({'type': 'sys_message', 'msg': msg_obj.text })
       }

       if(msg_obj.type == 'message'){
         console.log('new message')
         self.messages.unshift({ 'type': 'player_message', 'player': msg_obj.player_id, 'time': msg_obj.time, 'msg': msg_obj.text })
       }
         //self.socket.close();
     };

     self.socket.onclose = function() {
         self.socket = new SockJS(this.ws_server, 'websocket', {debug: true});
         console.log('close');
     };

  }
}
</script>
<style>
@media only screen and (max-width: 800px) {
  #board {
      position: relative; /* or absolute */
      height:80vh;
      padding: 2%;
      /*transform: translate(-50%, -50%);*/
  }
}

@media only screen and (min-width: 800px) {
  #board {
      position: absolute;; /* or absolute */
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
  }
}

.message-board {
  position: relative;
  max-height: 200px;
  overflow-y: scroll;
  padding: 2%;
}
.msg_area {
  width:100%;
  background: #03A9F4;
  color:#fff;
}

.me {
  background: #03A9F4;
  color: #fff;
  float:right;
  right:0;
  padding:2%;
}

.remote {
  background: #009688;
  left:0;
  color: #fff;
  float:left;
  padding:2%;
}

.sys_message {
  background: red;
  color:#fff;
  margin: auto;
  width: 100%;

}
</style>
