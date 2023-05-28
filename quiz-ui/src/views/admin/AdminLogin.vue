<template>
    <section class="h-100 gradient-form">
    <div class="container py-5 h-100">
        <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-xl-10">
            <div class="card rounded-3 text-black">
            <div class="row g-0">
                <div class="col-lg-6">
                <div class="card-body p-md-5 mx-md-4 text">

                    <div class="text-center">
                    <img src="../../assets/admin-icon.ico" alt="logo" class="icon">
                    <h4 class="mt-2 mb-5 pb-1">We are Team 7</h4>
                    </div>

                    <div>
                        <p>Please login to your account</p>
                        <div class="form-outline mb-4">
                            <input type="password" id="password" class="form-control" placeholder="Password" v-model="password" />
                        </div>

                        <div class="text-center pt-1 mb-5 pb-1 d-flex flex-column">
                            <button class="btn btn-color btn-block fa-lg gradient-custom-2 mb-3" @click="logIn">
                                Log in
                            </button>
                        </div>
                        <div v-if="showError" :class="hide">
                            <div class="alert alert-danger" role="alert">
                                ERROR : wrong password !
                            </div>
                        </div>
                    </div>

                </div>
                </div>
                <div class="bg-admin col-lg-6 d-flex align-items-center gradient-custom-2">
                </div>
            </div>
            </div>
        </div>
        </div>
    </div>
    </section>
</template>

<script>
    import quizApiService from "@/services/QuizApiService";

    export default {
        name: "AdminLogin",
        data() {
            return {
                password: "",
                showError: false,
            }
        },
        methods: {
            async logIn() {
                const login = await quizApiService.login({password: this.password});
                try {
                    if (login.status === 200) {
                        window.localStorage.setItem("token", login.data.token);
                        this.$router.push("/admin-panel");
                    }
                } catch (err) {
                    this.showError = true;
                }
            }
        }
    }
</script>

<style scoped>
    section {
        width: 100%;
        height: 100%;
    }

    .icon {
        width: 20%
    }

    .text {
        font-family: 'Helvetica';
    }

    .btn-color {
        background-color: #0001FC;
        color: white
    }

    .bg-admin {
        background: url('../../assets/admin-BG.jpg') no-repeat center center;
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        background-size: cover;
    }

    .hide {
        display: none;
    }
</style>