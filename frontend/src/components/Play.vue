<template>
  <div id="game">
    <div id="board" >
    <span v-if="player.role">You've joined as {{player.role}}</span><br />
    <span v-if="positionInfo">Now it's {{positionInfo.turn}}'s turn</span>
    <chessboard v-if="player.role == 'white'" @onMove="showInfo" :fen="currentFen" :onPromotion="promote"></chessboard>
    <chessboard v-if="player.role == 'black'" orientation="black" @onMove="showInfo" :fen="currentFen" :onPromotion="promote"  ></chessboard>
    <chessboard v-if="player.role == 'watcher'" :fen="currentFen" style="pointer-events: none"></chessboard>
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
      socket: null
    }
  },
  methods: {
    showInfo(data) {
        let self = this
        if(self.socket) {
          self.socket.send(JSON.stringify({'type': 'new_move', 'player': self.player.role, 'room': self.room, 'fen': data.fen}))
        }

        this.positionInfo = data
        console.log(self.positionInfo)
        if(self.positionInfo.turn == self.player.role) {
            console.log('enable click')
               document.getElementById("board").style.pointerEvents = "auto";
          } else {
            console.log('disable click')
               document.getElementById("board").style.pointerEvents = "none";
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
     this.socket = new SockJS('/ws', 'websocket', {debug: true});
     this.socket.onopen = function() {
     console.log('connected');
          var t=setInterval(function() { self.socket.send(
            JSON.stringify({
              type: "keepalive",
            })
          );
        },1000);
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
         //self.socket.close();
     };

     self.socket.onclose = function() {
         self.socket = new SockJS('/ws', 'websocket', {debug: true});
         console.log('close');
     };

  }
}
</script>
<style>
#board {
    position: fixed; /* or absolute */
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>
