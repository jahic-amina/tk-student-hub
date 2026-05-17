<template>
  <div class="max-w-4xl mx-auto py-8 px-4">

    <div v-if="loading" class="text-center py-20 text-gray-400"> Učitavanje...</div>

    <div v-else-if="error" class="bg-red-100 text-red-600 p-4 rounded-lg">
       {{ error }} </div>
    
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