<template>
    <div class="d-flex flex-column align-content-between" style="width: 60%">
        <div class="form-area shadow-lg center">
            <div class="d-flex justify-content-end">
                <button class="btn btn-warning" style="margin-right: 2px" @click="editQuestion(position)"> Edit </button>
                <button class="btn btn-danger" @click="deleteQuestion()"> Delete </button>
            </div>
            <form style="margin-top: 2%;">
                <div class="row">
                    <div class="form-group row">
                        <label for="Title" class="col-sm-2 col-form-label" style="color:black">Title : </label>
                        <div class="col-sm-10">
                            <input type="email" class="form-control" id="Title" placeholder="Title"  v-model="title" disabled>
                        </div>
                    </div>
                    <div class="form-group row" style="margin-top: 2%">
                        <label for="Title" class="col-sm-2 col-form-label" style="color:black">Entitled : </label>
                        <div class="col-sm-10">
                            <input type="email" class="form-control" id="Entitled" placeholder="Entitled"  v-model="text" disabled>
                        </div>
                    </div>
                    <div class="form-group row" style="margin-top: 2%">
                        <label for="Title" class="col-sm-2 col-form-label" style="color:black">Answers : </label>
                        <div class="col-sm-10">
                            <div v-for="(answer, index) in answers" class="col d-flex justify-content-start">
                                <input class="form-check-input" :value="index" type="radio" name="answer1Radio" id="answer1Radio"  v-model="correctIDX" :checked="answer.isCorrect" @change="updateCorrectAnswer()">
                                <input type="text" class="as-label" v-model="answer.text"  />
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
    import quizApiService from "@/services/QuizApiService";

    export default {
        name: "AdminDetailQuestion",
        data() {
            return {
                id: 0,
                correctIDX: 0,
                title: "",
                text: "",
                position: 0,
                image: "",
                answers: []
            }
        },
        async created() {
            const questionInfo = await quizApiService.getQuestion(this.$route.query.data);
            if (questionInfo.status !== 200) console.log("ERROR: CAN'T GET QUESTION INFO");

            this.id = questionInfo.data[0].id;
            this.title = questionInfo.data[0].title;
            this.text = questionInfo.data[0].text;
            this.position = questionInfo.data[0].position;
            this.image = questionInfo.data[0].image;
            this.answers = questionInfo.data[0].possibleAnswers;
        },
        methods: {
            async deleteQuestion() {
                try {
                    await quizApiService.deleteQuestion(this.id, window.localStorage.getItem("token"));
                    this.$router.push('/admin-panel');
                } catch (err) {
                    console.log(err);
                }
            },
            editQuestion(data) {
                this.$router.push({ name: "editQuestion", query: { data } });
            },
            async updateCorrectAnswer() {
                for (let i = 0; i < this.answers.length; ++i)
                    this.answers[i].isCorrect = i == this.correctIDX
                    
                await quizApiService.updateQuestion(this.id, {
                    "title": this.title,
                    "text": this.text,
                    "position": this.position,
                    "image": this.image,
                    "possibleAnswers": this.answers} , window.localStorage.getItem("token"))
                
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