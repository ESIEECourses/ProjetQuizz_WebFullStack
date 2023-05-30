<template>
    <div class="d-flex flex-column align-content-between" style="width: 60%">
        <div class="form-area shadow-lg center">
            <div class="d-flex justify-content-end">
                <router-link class="btn btn-primary"  to="new-question"> Create </router-link>
            </div>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Title</th>
                        <th scope="col">Text</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="data" v-for="question in questions" @click="getDetail(question.position)">
                        <th v-if="question" scope="row">{{ question.position }}</th>
                        <td v-if="question">{{ question.title }}</td>
                        <td v-if="question">{{ question.text }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
    import quizApiService from "@/services/QuizApiService";

    export default {
        name : "AdminPanel",
		data() {
			return {
				questions: [],
			}
		},
        async created() {
            const quizInfo = await quizApiService.getQuizInfo();
            if (quizInfo.status !== 200) console.log("ERROR: CAN'T GET QUIZ INFO");
            for (let i = 0; i < quizInfo.data.size; ++i)
                this.addNewQuestion(i + 1);
            
        },
        methods: {
            async addNewQuestion(pos) {
                const questionInfo = await quizApiService.getQuestion(pos);
                if (questionInfo === undefined || questionInfo.status !== 200) 
                {
                    console.log("ERROR: CAN'T GET QUESTION INFO");
                    return
                }
                
                this.questions[pos - 1] = questionInfo.data;
            },
            getDetail(data) {
                this.$router.push({ name: "detailQuestion", query: { data } });
            }
        }
    }
</script>

<style scoped>
    .data{
        cursor: pointer;
    }

    .data:hover {
        background-color: lightgrey;
    }
</style>