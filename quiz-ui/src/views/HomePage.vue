<template>
  <div class="d-flex flex-column align-content-between" style="width: 60%">
    <div class="center">
      <h1 class="title"> Welcome to our Mario Quiz !</h1>
      <div v-for="scoreEntry in registeredScores.slice(0,3)" v-bind:key="scoreEntry.date" class="home-text">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </div>
      <router-link class="button btn-small" to="/quiz">Begin quiz !</router-link>
    </div>
    
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: []
    };
  },
  async created() {
    const info = await quizApiService.getQuizInfo();
    if (info.status !== 200) console.log("ERROR : CAN'T LOAD DATA !");
  
    this.registeredScores = info.data.scores;
  }
};

</script>

<style>  
  .title{
    font-family: "Super Mario";
    color: white;
    font-weight: bold;
    text-shadow: -1px -1px white, 1px 1px black;
    margin-bottom: 10%;
  }

  .center {
    text-align: center;
  }

  .btn-small {
    width: 60% !important
  }

  .home-text {
    font-family: "Super Mario";
    font-weight: regular;
    color: white;
    text-shadow: -1px -1px white, 1px 1px black;
    font-size: 25px;
    margin-bottom: 5%
  } 
</style>