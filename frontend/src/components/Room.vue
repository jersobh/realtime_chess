<template>
    <div id="room" >
    <input type="text" v-model="room_name" placeholder="Digite o nome da sala" /> <router-link :to="'/'+room_name">Entrar</router-link>
    <table>
     <thead>
       <tr>
         <th>
           Room
         </th>
         <th>
           Players
         </th>
         <th>

         </th>
       </tr>
     </thead>
     <tbody>
       <tr v-for="(room, index) in rooms">
         <td >
           {{index}}
         </td>
         <td >
           Users: {{room.sessions.length}}
         </td>
         <td >
           <router-link :to="'/'+index">Join</router-link>
         </td>
       </tr>
     </tbody>
   </table>
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
      rooms: null,
      room_name:''
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
     self.socket.send(JSON.stringify({'type': 'get_rooms'}))
     };

     self.socket.onmessage = function(e) {
         let msg_obj;
          console.log(e.data)
          console.log(typeof e.data)
          if (typeof e.data == 'string') {
            msg_obj = JSON.parse(e.data)
          } else {
            msg_obj = e.data
          }
          self.rooms = msg_obj
         console.log(msg_obj)
         //let obj = JSON.parse(e.data)
         console.log(msg_obj)
         //self.socket.close();
     };

     self.socket.onclose = function() {
         self.socket = new SockJS('/ws');
         console.log('close');
     };

  }
}
</script>
