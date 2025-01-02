from io import BufferedRandom

def get_stack_address_range(pid: str) -> tuple[int, int]:
    with open(f"/proc/{pid}/maps", "r") as maps_file:
        for line in maps_file:
            if line.strip().endswith("[stack]"):
                start_address, end_address = line.split()[0].split("-")
                return int(start_address, 16), int(end_address, 16)
    raise ValueError("Stack address range not found")

def search_int_in_memory(memory: BufferedRandom, target_value: int, start_address: int, end_address: int) -> list[int]:
    found_addresses = []
    memory.seek(start_address)

    while memory.tell() < end_address:
        chunk = memory.read(4)
        if not chunk:
            break

        value = int.from_bytes(chunk, byteorder="little")
        if value == target_value:
            found_addresses.append(memory.tell() - 4)

    return found_addresses

def read_ints_from_memory(memory: BufferedRandom, addresses: list[int]) -> list[int]:
    values = []
    for address in addresses:
        memory.seek(address)
        values.append(int.from_bytes(memory.read(4), byteorder="little"))
    return values

def main():
    pid = input("Enter PID: ")
    initial_value = int(input("Enter the initial value: "))
    start_address, end_address = get_stack_address_range(pid)

    with open(f"/proc/{pid}/mem", "rb+") as memory:
        addresses = search_int_in_memory(memory, initial_value, start_address, end_address)

        while len(addresses) > 1:
            print(f"Total addresses ({len(addresses)}):", [f"{address:#x}" for address in addresses])

            new_value = input("Enter new value (input 'q' to exit loop): ")
            if new_value.lower().startswith("q"):
                print("Exiting loop")
                return
            new_value = int(new_value)

            memory_values = read_ints_from_memory(memory, addresses)
            addresses = [address for address, mem_v in zip(addresses, memory_values) if mem_v == new_value]

        print("Only one address left... exiting loop")
        edit_it = input(f"Do you wish to edit this address? {addresses[0]:#x} (y/n): ").lower()
        if not edit_it.startswith("y"):
            print("Exiting...")
            return

        while True:
            change_to = input("What value to change it to? (input 'q' to exit): ")
            if change_to.lower().startswith("q"):
                print("Exiting...")
                break

            change_to = int(change_to)
            memory.seek(addresses[0])
            memory.write(change_to.to_bytes(4, byteorder="little"))
            memory.flush()

            print("Value changed successfully!")

if __name__ == "__main__":
    main()
