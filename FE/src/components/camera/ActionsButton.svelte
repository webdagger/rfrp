<script lang="ts">
    import { SaveIcon, Trash2Icon } from 'svelte-feather-icons'
</script>

<div>
        <button>
            <span>
                <SaveIcon size='1x' />
            </span>
            Add User Photo
        </button>

        <button>
            <span>
                <Trash2Icon size='1x' />
            </span>
            Delete User Data
        </button>
    
</div>

<style lang="scss">
    div {
        display: flex;
        justify-content: center;
        align-items: center;
        box-sizing: content-box;
        text-align: center;
    }

    button {
        display: flex;
        margin: 1rem;
        padding: 1rem;
        span {
            padding-right: 5px;
        }
    }
</style>