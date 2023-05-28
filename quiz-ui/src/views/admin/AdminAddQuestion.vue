<template>
    <div class="d-flex flex-column align-content-between" style="width: 60%">
        <div class="form-area shadow-lg center">
            <form>
                <div class="row">
                    <div class="col">
                        <input type="text" class="form-control" placeholder="Title" v-model="title" required>
                    </div>
                    <div class="col">
                        <input type="text" class="form-control" placeholder="Entitled" v-model="text" required>
                    </div>
                </div>
                <div class="row" style="margin-top: 2%">
                    <div class="col">
                        <input type="text" class="form-control" placeholder="Image" v-model="image">
                    </div>
                    <div class="col">
                        <input type="text" class="form-control" placeholder="Position" v-model="position" disabled>
                    </div>
                </div>
                <div class="row" style="margin-top: 2%">
                    <div class="col d-flex justify-content-start">
                        <input class="form-check-input" type="radio" name="answer" id="answer1Radio" value="0" checked>
                        <input type="text" class="as-label" v-model="answers[0]" required/>
                    </div>
                    <div class="col d-flex justify-content-start">
                        <input class="form-check-input" type="radio" name="answer" id="answer2Radio" value="1">
                        <input type="text" class="as-label" v-model="answers[1]" required/>
                    </div>
                    <div class="col d-flex justify-content-start">
                        <input class="form-check-input" type="radio" name="answer" id="answer3Radio" value="2">
                        <input type="text" class="as-label" v-model="answers[2]"  required />
                    </div>
                    <div class="col d-flex justify-content-start">
                        <input class="form-check-input" type="radio" name="answer" id="answer4Radio" value="3">
                        <input type="text" class="as-label" v-model="answers[3]" required/>
                    </div>
                </div>
            </form>
            <div class="d-flex justify-content-center" style="margin-top: 2%">
                <router-link to="/admin-panel" class="btn btn-secondary" style="margin-right: 2%"> Return </router-link>
                <button class="btn btn-primary" @click="addNewQuestion"> Create </button>
            </div>
        </div>
    </div>
</template>


<script>
import quizApiService from '@/services/QuizApiService';

    export default {
        name: "AdminAddQuestion",
        data() {
			return {
				title: "",
                text: "",
                position: "",
                image: "",
                answers: []
			}
		},
        async created() {
            // init position
            const quizInfo = await quizApiService.getQuizInfo();
            if  (quizInfo.status !== 200) console.log("ERROR: CAN'T GET QUIZ INFO");

            this.position = quizInfo.data.size + 1;
        },
        methods: {
            async addNewQuestion() {
                // handle answers
                let correctAnswer = parseInt(document.querySelector('input[name="answer"]:checked').value);
                let possibleAnswers = [];
                for (let i = 0; i < 4; ++i)
                {
                    possibleAnswers.push({
                        "text": this.answers[i] !== undefined ? this.answers[i] : '',
                        "isCorrect": correctAnswer == i
                    });
                }

                let data = {
                    "title": this.title,
                    "text": this.text,
                    "image": this.image,
                    "position": this.position,
                    "possibleAnswers": possibleAnswers
                }

                await quizApiService.addQuestion(data, window.localStorage.getItem("token"));
                this.$router.push("/admin-panel");
            }
        }
    }
</script>

<style scoped>
    .as-label {
        margin-left: 5px;
        border: none !important;
    }

    .as-label:focus-visible {
        outline: none!important;
    }
</style>