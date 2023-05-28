<template>
    <div class="d-flex flex-column align-content-between" style="width: 60%">
        <div class="form-area shadow-lg center">
            <form style="margin-top: 2%;">
                <div class="row">
                    <div class="col">
                        <input type="text" class="form-control" placeholder="Title" v-model="title">
                    </div>
                    <div class="col">
                        <input type="text" class="form-control" placeholder="Entitled" v-model="text">
                    </div>
                </div>
                <div class="row" style="margin-top: 2%">
                    <div class="col">
                        <input type="text" class="form-control" placeholder="Image" v-model="image">
                    </div>
                    <div class="col">
                        <input type="text" class="form-control" placeholder="Position" v-model="position">
                    </div>
                </div>
                <div class="row" style="margin-top: 2%">
                    <div v-for="(answer, index) in answers" class="col d-flex justify-content-start">
                        <input class="form-check-input" :value="index" type="radio" name="answer1Radio" id="answer1Radio" v-model="correctIDX" :checked="answer.isCorrect">
                        <input type="text" class="as-label" v-model="answer.text"  />
                    </div>
                </div>
            </form>
            <div class="d-flex justify-content-center" style="margin-top: 2%">
                <router-link to="/admin-panel" class="btn btn-warning" style="margin-right: 2%"> Cancel </router-link>
                <button class="btn btn-primary" @click="updateQuestion()"> Save </button>
            </div>
        </div>
    </div>
</template>

<script>
    import quizApiService from "@/services/QuizApiService";

    export default {
        name: "AdminEditQuestion",
        data() {
            return {
                id: 0,
                correctIDX: 0,
                title: "",
                text: "",
                position: 0,
                image: "",
                answers: [],
            }
        },
        async created() {
            const questionInfo = await quizApiService.getQuestion(this.$route.query.data);
            if (questionInfo.status !== 200) console.log("ERROR: CAN'T GET QUESTION INFO");

            this.id = questionInfo.data[0].id;
            this.title = questionInfo.data[0].title;
            this.text = questionInfo.data[0].text;
            this.position = questionInfo.data[0].position;
            this.image = questionInfo.data[0].image
            this.answers = questionInfo.data[0].possibleAnswers
        }, 
        methods: {
            async updateQuestion() {
                for (let i = 0; i < this.answers.length; ++i)
                    this.answers[i].isCorrect = i == this.correctIDX
                                    
                    
                await quizApiService.updateQuestion(this.id, {
                    "title": this.title,
                    "text": this.text,
                    "position": this.position,
                    "image": this.image,
                    "possibleAnswers": this.answers} , window.localStorage.getItem("token"))

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