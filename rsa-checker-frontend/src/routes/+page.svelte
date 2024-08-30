<script>
  import { onMount } from 'svelte';

  let testCenters = [];
  let search = '';
  let sort = 'az';
  let order = 'asc';
  let lastUpdatedDate = '';

  onMount(fetchData);

  async function fetchData() {
    const response = await fetch(`http://127.0.0.1:5000/api/test-centers?search=${search}&sort=${sort}&order=${order}`);
    testCenters = await response.json();
    updateLastUpdatedDate();
  }

  function updateLastUpdatedDate() {
    if (testCenters.length > 0) {
      const earliestDate = testCenters.reduce((earliest, center) => {
        const centerDate = new Date(center['Last Updated']);
        return centerDate < earliest ? centerDate : earliest;
      }, new Date(testCenters[0]['Last Updated']));
      lastUpdatedDate = formatDate(earliestDate);
    } else {
      lastUpdatedDate = 'N/A';
    }
  }

  function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB', { day: '2-digit', month: '2-digit', year: 'numeric' });
  }
</script>

<main class="container mx-auto px-4 py-8">
  <h1 class="text-2xl sm:text-3xl font-bold mb-6 text-center text-purple-600">Unofficial RSA Driving Test Booking Checker</h1>
  <h3 class="text-lg sm:text-xl font-semibold mb-4 text-center text-gray-600">Find out when you can book your RSA driving test</h3>
  <h6 class="mb-4 text-center"><i>Last Updated: </i><i>{lastUpdatedDate}</i></h6>

  <div class="text-center mb-6">
    <a href="http://127.0.0.1:5000/api/test-centers" target="_blank" 
       class="inline-block px-6 py-2 text-white bg-purple-600 hover:bg-purple-700 rounded-md text-lg font-semibold">
      View API Data
    </a>
  </div>

  <div class="mb-6 flex flex-col space-y-4">
    <input 
      type="text" 
      bind:value={search}
      on:input={fetchData}
      placeholder="Search test centers..." 
      class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
    >
    <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
      <select 
        bind:value={sort}
        on:change={fetchData}
        class="w-full sm:w-1/2 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        <option value="az">Sort A-Z</option>
        <option value="date">Sort by Date</option>
      </select>
      <select 
        bind:value={order}
        on:change={fetchData}
        class="w-full sm:w-1/2 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        <option value="asc">Ascending</option>
        <option value="desc">Descending</option>
      </select>
    </div>
  </div>

  <div class="bg-white shadow-md rounded-lg overflow-x-auto">
    <table class="w-full">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Test Centre</th>
          <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Expected Invite</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        {#each testCenters as center}
          <tr>
            <td class="px-4 py-4 whitespace-nowrap text-sm">{center['Test Centre']}</td>
            <td class="px-4 py-4 whitespace-nowrap text-sm">{formatDate(center['Expected Invite'])}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</main>