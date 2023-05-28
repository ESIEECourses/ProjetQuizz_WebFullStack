<template>
  <div class="d-flex flex-column align-content-between" style="width: 60%">
    <div class="form-area shadow-lg center">
      <h1 class ="form-title mb-5"> Write your name </h1>
      <form class="center">
        <div class="form-group">
          <input type="text" class="form-control mb-5" id="inputUsername" placeholder="Username" v-model="username">
        </div>

      <button type="submit" class="button" @click="launchNewQuiz">Play</button>
    </form>
    </div>
    
  </div>
  
  
</template>

<script>
  import ParticipationStorageService from "@/services/ParticipationStorageService";
  export default {
    name: "QuizPage",
    data() {
      return {
        username: ''
      };
    },
    methods:{
      launchNewQuiz() {
        ParticipationStorageService.savePlayerName(this.username);
        this.$router.push('/questions');
      }
    }
  };

</script>

<style>  
  .form-area {
    background-color: white;
    padding: 5%;
    border-radius: 2%;
  }

  .button {
    width: 80%
  }

  .center {
    text-align: center;
  }

  .mb-5 {
    margin-bottom: 5%;
  }

  .form-title {
    color: gray;
    font-family: "Press Start 2p";
    font-weight: bold;
    text-shadow: -1px -1px white, 1px 1px black;
  }
</style>