<template>
    <h1 class ="form-title mb-5 font-12"> {{ question.title }} </h1>
    <h3 class="sub-title mb-5"> {{ question.text }}   </h3>
    <img v-if="question.image" :src="question.image" >
    <div class="text d-flex flex-column align-items-center">
        <div class="form-check" v-for="(answer, idx) in question.possibleAnswers" :key="idx">
            <input class="form-check-input" type="radio" name="radio" @change="onChecked(idx)"/>
            <label class="form-check-label">
                {{ answer.text }} 
            </label>
        </div>

        <button class="button mt-5" @click="$emit('answer-selected', selectedIDX)">Next</button>
    </div>
</template>

<script>
    export default {
        name: "QuestionDisplay",
        emits: ["answer-selected"],
        data() {
            return {
                selectedIDX: null
            };
        },
        props: {
            question: {
                type: Object
            }
        },
        methods:{
            onChecked(idx) {
                this.selectedIDX = idx;
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

  .mt-5 {
    margin-top: 5%;
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

  .sub-title {
    color: black;
    font-family: "Press Start 2p";
    font-size: 11px;
  }

  .text {
    color: black;
    font-family: "Super Mario";
    font-weight: 200;
  }

  .font-12 {
    font-size: 12px
  }
</style>