<script setup lang="ts"></script>

<template>
  <footer class="footer-wapper">
    <div class="footer">
      <div class="divider">
        <p>脚标：还没想好</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer-wapper {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  height: 200px;
  background-color: #f8f9fa;
  margin-top: 20px;
  padding: 20px;
}

.footer {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  white-space: nowrap;
  width: 100%;
}

.divider {
  display: flex;
  width: 80%;
  align-items: center;
  justify-content: center;
  flex-direction: row;
  margin: 0 1rem;
}

.divider::before {
  content: '';
  flex: 1;
  height: 1px;
  border-top: 1px solid #9d9d9d;
  margin-inline-end: 2rem;
}

.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  border-top: 1px solid #9d9d9d;
  margin-inline-start: 2rem;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;

  p {
    margin: 0;
    font-size: 1rem;
    font-weight: bold;
    text-align: center;
  }

  img {
    height: 100px;
    width: 100%;
  }
}

.logo:hover {
  text-decoration: none;
}

.info {
  display: flex;
  flex-direction: column;
  font-size: 1.2rem;

  * {
    margin: 0.5rem;
  }

  a {
    text-decoration: underline;
    margin: 0 0.5rem;
  }
}

@media screen and (max-width: 1080px) {
  .footer-wapper {
    flex-direction: column;
    height: 150px;
  }

  .footer-img {
    height: 100px;
  }

  .info {
    font-size: 1rem;
  }

  .info > * {
    margin: 0.3rem;
  }
}
</style>
