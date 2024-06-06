<script setup lang="ts"></script>

<template>
  <header>
    <div class="tittle-bar">
      <div class="tittle-warper">
        <RouterLink to="/">
          <img src="@/assets/images/logo.svg" class="go-back-icon" />
        </RouterLink>
        <div class="title">
          <p>图书预约系统</p>
        </div>
        <div class="user-info">
          <RouterLink to="/login">登录</RouterLink>
          <RouterLink to="/profile">个人中心</RouterLink>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.tittle-bar {
  height: 80px;
  background-color: #005826;
}

.tittle-warper {
  display: flex;
  height: 100%;
  margin: auto 320px;
  align-items: center;
}

.go-back-icon {
  margin-top: 0.3rem;
  height: 4rem;
  vertical-align: middle;
}

.title {
  color: #fff;
  vertical-align: middle;

  p {
    font-size: 2rem;
    font-weight: 500;
  }
}

.user-info {
  color: #fff;
  margin-left: auto;
  font-size: 1.2rem;
}

@media screen and (max-width: 1080px) {
  .tittle-bar {
    height: 60px;
  }

  .tittle-warper {
    margin: auto 10px;
  }

  .go-back-icon {
    height: 3rem;
  }

  .title {
    p {
      font-size: 1.5rem;
    }
  }
}
</style>
