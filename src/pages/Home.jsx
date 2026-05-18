import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import Header from "@/components/header"
import { Heart } from "lucide-react"
import LikeButton from "@/components/likeButton"
import { timeAgo } from "@/utils/timeAgo"
import AvatarUpload from "@/components/avatarUpload"

export default function Home() {
    const [posts, setPosts] = useState([])
    const [content, setContent] = useState("")
    const [loading, setLoading] = useState(true)
    const [posting, setPosting] = useState(false)
    const navigate = useNavigate()
    const token = localStorage.getItem("token")

    useEffect(() => {
        fetchPosts()
    }, [])

    useEffect(()=> {
        
    })

    async function fetchPosts() {
        try {
            const res = await fetch(`${import.meta.env.VITE_URL_API}/posts/`, {
                headers: { "Authorization": `Bearer ${token}` }
            })
            const data = await res.json()
            setPosts(data)
            console.log(data)

        } catch {
            console.error("Impossible de charger les posts")
        } finally {
            setLoading(false)
        }
    }

    async function handlePost() {
        if (!content.trim()) return
        setPosting(true)
        try {
            const res = await fetch(`${import.meta.env.VITE_URL_API}/posts/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify({ content }),
            })
            if (res.ok) {
                setContent("")
                await fetchPosts()
            }
        } catch {
            console.error("Impossible de publier")
        } finally {
            setPosting(false)
        }
    }

    function handleLogout() {
        localStorage.removeItem("token")
        navigate("/login")
    }

    return (
        <div className="min-h-screen bg-gray-100">
            <Header logout={handleLogout} />

            <main className="max-w-3xl mx-auto py-8 px-4 flex flex-col gap-6">
                <Card className="mt-20">
                    <CardContent className="pt-4">
                        <textarea
                            className="w-full resize-none bg-transparent outline-none text-sm min-h-20"
                            placeholder="Quoi de neuf ?"
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                        />
                        <div className="flex justify-end mt-2">
                            <Button size="sm" disabled={!content.trim() || posting} onClick={handlePost}>
                                {posting ? "Publication..." : "Publier"}
                            </Button>
                        </div>
                    </CardContent>
                </Card>
                <div className="text-2xl font-bold">Feeds</div>
                {loading ? (
                    <p className="text-sm text-muted-foreground text-center">Chargement...</p>
                ) : posts.length === 0 ? (
                    <p className="text-sm text-muted-foreground text-center">Aucun post pour l'instant.</p>
                ) : (

                    posts.map((post) => (
                        <Card key={post.id}>
                            <CardHeader className="pb-2">
                                <CardTitle className="flex items-center gap-2">
                                    <Avatar className="h-10 w-10">
                                        <AvatarImage src={`${import.meta.env.VITE_URL_API}/uploads/${post.profil_photo}`} className="object-cover" />
                                        <AvatarFallback>{post.pseudo?.[0]?.toUpperCase() ?? "?"}</AvatarFallback>
                                    </Avatar>
                                    <div>
                                        <p className="text-sm font-semibold">{post.pseudo}</p>
                                        <p className="text-xs text-gray-400">{timeAgo(post.creation_date)}</p>
                                    </div>
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm">{post.content}</p>
                                <div className="flex content-between mt-8">
                                    <LikeButton />
                                </div>
                            </CardContent>
                        </Card>
                    ))
                )}
            </main>
        </div>
    )
}
