import { Heart } from "lucide-react";
import { useState } from "react";

export default function LikeButton() {
  const [liked, setLiked] = useState(false);

  return (
    <button className="hover:scale-110 transition" onClick={() => setLiked(!liked)}>
      <Heart
        size={28}
        strokeWidth={1.5}
        className={`transition ${
          liked
            ? "text-red-500 fill-red-500"
            : "text-gray-500"
        }`}
      />
    </button>
  );
}