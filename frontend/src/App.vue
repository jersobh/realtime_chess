<template>
  <div id="app">
    <router-view/>
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
    positionInfo: function (newVal, oldVal) {
      let self = this
      console.log('new move')
      if(newVal !== oldVal) {
        console.log(newVal)
        self.socket.send(JSON.stringify({'fen': newVal.fen}))
      }
    }
  },
  data () {
    return {
      currentFen: '',
      positionInfo: null,
      player: 'white',
      socket: null,
      uuid: null
    }
  },
  methods: {
    uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
    },
    showInfo(data) {
        let self = this
        this.positionInfo = data

    },
    resetGame() {
    if (confirm("Want to promote to rook? Queen by default") ) {
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

  },
  mounted () {
     let self = this
     this.socket = new SockJS('/ws');
     this.socket.onopen = function() {
     console.log('connected');
          var t=setInterval(function() { self.conn.send(
            JSON.stringify({
              type: "keepalive",
              peer_id: self.uuid
            })
          );
        },1000);
          self.conn.send(
            JSON.stringify({
              type: "new_peer",
              peer: self.uuid,
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
         console.log(msg_obj)
         //let obj = JSON.parse(e.data)
         self.currentFen = e.data.fen
         //self.socket.close();
     };

     self.socket.onclose = function() {
         self.socket = new SockJS('/ws');
         console.log('close');
     };

  }
}
</script>
<style>
.btn {
  background-color: white;
  color: #333;
  border: 2px solid #008CBA;
  border: none;
  padding: 16px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  -webkit-transition-duration: 0.4s; /* Safari */
  transition-duration: 0.4s;
  cursor: pointer;
}

.btn:hover {
  background-color: #008CBA !important;
  color: white  !important;;
}
</style>
