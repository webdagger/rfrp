
<div>
    <form on:submit|preventDefault={ handleSubmit }>
        <div class="personal">
            <div class="errors"></div>
            <div class="name">
                <h3>Name</h3>
                    <input bind:value="{ firstname }" type="text" id="firstname" placeholder="First Name" />
                    <input bind:value="{ lastname }" type="text" id="lastname" placeholder="Last Name">
            </div>

            <div class="image">
                <label for="image">
                    Test image
                    <input
                      bind:value="{ image }"
                      accept="image/png, image/jpeg"
                      type="file" id="image"
                    />
                </label>
            </div>
        </div>

        <div class="consent">
            <label for="choose">Choose to preserve data for 1 month?</label>
            <select  id="choose">
              <option disabled selected>Please select</option>
              <option on:click="{ consent = true }" value="keep">Preserve?</option>
              <option on:click="{ consent = false }"value="delete">Delete after 5mins.</option>
            </select>
        </div>

        <input class="submit" type="submit" value="Submit">
        <button class="loading hidden">
            <Jumper size="60" color="#FF3E00" unit="px" duration="1s"></Jumper>

        </button>
      </form>
</div>

<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { Jumper } from 'svelte-loading-spinners'

  const dispatch = createEventDispatcher();

    let firstname: string;
    let lastname: string;
    let image;
    let consent: bool = false;
    let loadingButton = document.querySelector('loading');
    let submitButton = document.querySelector('submit');

    async function handleSubmit() {
        submitButton.classList.add('hidden');
        loadingButton.classList.remove('hidden');

        const formData = new FormData();
        formData.append('first_name', firstname);
        formData.append('last_name', lastname);
        formData.append('image_array', image[0]);
        formData.append('email', 'email@mail.com')
        formData.append('organization', '603e1fdb0cf8ae852a40150f')
        console.log(formData)
        let res = await fetch('https://localhost:8080/',{
            method: 'POST',
            body: formData
        }).then((response) => response.json())
        .then((result) => {
            console.log(result);
        })
        .catch((error) => {
            console.log(error);
        })
    }

</script>
<slot />

<style lang="scss">
    form {
        display: flex;
        flex-direction: column;
        margin: 1rem;
        align-content: space-around;
        div {
            padding-top: 1rem;

        }
        input {
            margin-top: 1rem;
        }
    }

    .personal {
        display: flex;
        flex-direction: column;
        min-height: 40%;
        justify-content: center;
        .name {
            h3 {
                text-align: center;
            }
            input {
                padding: 5px;
                margin: 2px;
            }
        }

    }

    .consent {
        min-height: 20%;
        display: flex;
        flex-direction: column;
        text-align: center;
    }
</style>