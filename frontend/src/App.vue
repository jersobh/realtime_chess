<template>
  <div id="app">
    <div id="board" >
    <chessboard style="width:100vw; height:100vh;" v-if="player == 'white'" @onMove="showInfo" :fen="currentFen" :onPromotion="promote"></chessboard>
    <chessboard v-if="player == 'black'" orientation="black" @onMove="showInfo" :fen="currentFen" :onPromotion="promote"></chessboard>

    </div>
    <button @click="resetGame()">reset</button>
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
      socket: null
    }
  },
  methods: {
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
     console.log('open');
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
