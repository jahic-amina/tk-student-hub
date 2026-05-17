<template>
  <div>

    <div v-if="loading"> Učitavanje...</div>

    <div v-else-if="error"> {{ error }} </div>
    
    <div v-else-if="profile">
      <UserProfileCard :profile="profile" />
      <div>
        <h2>O meni</h2>
        <p>{{ profile.biografija || 'Nije unesena biografija.' }}</p>
      </div>

       <div>
          <h2>Trenutne prakse</h2>
          <p>Nema trenutnih praksi.</p>
        </div>

        <div>
          <h2>Nedavna aktivnost</h2>
          <p>Nema nedavne aktivnosti.</p>
        </div>

      </div>

    </div>

  </div>
</template>