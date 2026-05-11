import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

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

    async function fetchPosts() {
        try {
            const res = await fetch(`${import.meta.env.VITE_URL_API}/posts/`)
            const data = await res.json()
            setPosts(data)
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
        <div className="min-h-screen bg-background">
            <nav className="border-b px-6 py-3 flex items-center justify-between">
                <h1 className="text-lg font-semibold">Social Web</h1>
                <Button variant="outline" size="sm" onClick={handleLogout}>
                    Déconnexion
                </Button>
            </nav>

            <main className="max-w-xl mx-auto py-8 px-4 flex flex-col gap-6">
                <Card>
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

                {loading ? (
                    <p className="text-sm text-muted-foreground text-center">Chargement...</p>
                ) : posts.length === 0 ? (
                    <p className="text-sm text-muted-foreground text-center">Aucun post pour l'instant.</p>
                ) : (
                    posts.map((post) => (
                        <Card key={post.id}>
                            <CardHeader className="pb-2">
                                <CardTitle className="text-sm font-semibold">
                                    @{post.author}
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm">{post.content}</p>
                            </CardContent>
                        </Card>
                    ))
                )}
            </main>
        </div>
    )
}
