import { AvatarBadge } from "./ui/avatar";


const UserInfo = () => {

    return (
        <Avatar>
            <AvatarBadge
                src="https://github.com/shadcn.png"
                alt="@shadcn"
                className="grayscale"
            />
            <AvatarFallback>CN</AvatarFallback>
        </Avatar>
    )
}

export default UserInfo;