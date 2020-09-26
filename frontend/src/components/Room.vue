<template>
    <div id="room" >
    <input type="text" v-model="room_name" placeholder="Digite o nome da sala"  class="btn" /> <router-link :to="'/'+room_name"  class="btn">Entrar</router-link>
    <table class="rooms_table">
     <thead>
       <tr>
         <th>
           Room
         </th>
         <th>
           Users
         </th>
         <th>

         </th>
       </tr>
     </thead>
     <tbody>
       <tr v-for="(room, index) in rooms" :key="index">
         <td >
           {{index}}
         </td>
         <td >
           {{room.sessions.length}}
         </td>
         <td >
           <router-link :to="'/'+index" class="btn">Join</router-link>
         </td>
       </tr>
     </tbody>
   </table>
  </div>
</template>

<script>
import SockJS from 'sockjs-client'
export default {
  name: 'app',
  watch: {
    positionInfo: function (newVal, oldVal) {
      let self = this
      if(newVal !== oldVal) {
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
      room_name:'',
      ws_server: '/ws'
    }
  },
  methods: {
    showInfo(data) {
        let self = this
        self.positionInfo = data

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
     this.socket = new SockJS(this.ws_server);
     this.socket.onopen = function() {
          setInterval(function() { self.socket.send(
            JSON.stringify({
              type: "get_rooms",
            })
          );
        },2000);
     };

     self.socket.onmessage = function(e) {
         let msg_obj;
          if (typeof e.data == 'string') {
            msg_obj = JSON.parse(e.data)
          } else {
            msg_obj = e.data
          }
          self.rooms = msg_obj
     };

     self.socket.onclose = function() {
         self.socket = new SockJS(this.ws_server);
     };

  }
}
</script>
<style>
table.rooms_table {
  width: 100%;
  background-color: #FFFFFF;
  border-collapse: collapse;
  border-width: 2px;
  border-color: #222D42;
  border-style: solid;
  color: #333;
}

table.rooms_table td, table.rooms_table th {
  border-width: 2px;
  border-color: #222D42;
  border-style: solid;
  padding: 5px;
}

table.rooms_table thead {
  background-color: #7EA8F8;
}
</style>
