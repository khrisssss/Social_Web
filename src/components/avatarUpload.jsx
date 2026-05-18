import { useRef, useState, useEffect } from "react";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";

export default function AvatarUpload({ content = "Changer photo", imageProfil}) {
    const [image, setImage] = useState(null);
    const inputRef = useRef(null);

    // Ouvre le file picker
    const openFilePicker = () => {
        inputRef.current?.click();
    };

    // Handle upload image
    const handleUpload = (e) => {
        const file = e.target.files?.[0];
        if (!file) return;

        const url = URL.createObjectURL(file);
        setImage(url);
    };

    useEffect(()=> {
        if (imageProfil) {
            setImage(imageProfil)
        }

    },[])

    // Clean memory (bonne pratique)
    useEffect(() => {
        return () => {
            if (image) URL.revokeObjectURL(image);
        };
    }, [image]);

    return (
        <div className="flex items-center gap-4">

            <Avatar className="h-16 w-16">
                <AvatarImage src={image || ""} className="object-cover" />
                <AvatarFallback className="bg-gray-200 text-gray-600">
                    U
                </AvatarFallback>
            </Avatar>

            <input
                ref={inputRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleUpload}
            />

            <Button
                variant="outline"
                onClick={openFilePicker}
                className="cursor-pointer hover:scale-105 transition"
            >
                {content}
            </Button>

        </div>
    );
}