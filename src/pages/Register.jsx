import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"

export default function Register() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [prompt, setPrompt] = useState("")
    const [preview, setPreview] = useState(null)
    const [generating, setGenerating] = useState(false)
    const [error, setError] = useState("")
    const navigate = useNavigate()

    async function handleGenerate() {
        if (!prompt.trim()) return
        setGenerating(true)
        if (preview?.startsWith("blob:")) URL.revokeObjectURL(preview)
        setPreview(null)
        try {
            const encoded = encodeURIComponent(prompt.trim())
            const res = await fetch(
                `${import.meta.env.VITE_URL_API}/preview_image?prompt=${encoded}`
            )
            if (!res.ok) throw new Error(`Erreur ${res.status}`)
            const blob = await res.blob()
            setPreview(URL.createObjectURL(blob))
        } catch {
            setError("Impossible de générer l'image, réessaie.")
        } finally {
            setGenerating(false)
        }
    }

    async function handleSubmit(e) {
        e.preventDefault()
        setError("")
        try {
            const res = await fetch(`${import.meta.env.VITE_URL_API}/registration`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            })
            const data = await res.json()
            if (!res.ok) {
                setError(data.detail || "Erreur lors de l'inscription")
                return
            }

            if (preview) {
                const loginRes = await fetch(`${import.meta.env.VITE_URL_API}/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password }),
                })
                if (loginRes.ok) {
                    const { access_token } = await loginRes.json()
                    const payload = JSON.parse(atob(access_token.split(".")[1]))
                    const userId = payload.id

                    const imgRes = await fetch(preview)
                    const formData = new FormData()
                    formData.append("image", await imgRes.blob(), "profil.png")

                    await fetch(`${import.meta.env.VITE_URL_API}/upload?user_id=${userId}`, {
                        method: "POST",
                        body: formData,
                    })
                }
            }

            navigate("/login")
        } catch {
            setError("Impossible de contacter le serveur")
        }
    }

    return (
        <div className="flex min-h-screen items-center justify-center">
            <Card className="w-full max-w-sm">
                <CardHeader>
                    <CardTitle>Créer un compte</CardTitle>
                    <CardDescription>Choisissez un pseudo et un mot de passe</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-col items-center gap-3 mt-2 mb-6">
                        <Avatar className="h-20 w-20">
                            {preview && (
                                <AvatarImage
                                    src={preview}
                                    className="object-cover"
                                    onLoad={() => setGenerating(false)}
                                    onError={() => setGenerating(false)}
                                />
                            )}
                            <AvatarFallback className="bg-gray-200 text-gray-500 text-xs">
                                {generating ? "..." : "Photo"}
                            </AvatarFallback>
                        </Avatar>
                        <div className="flex w-full gap-2">
                            <Input
                                placeholder="Décris ta photo de profil…"
                                value={prompt}
                                onChange={(e) => setPrompt(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), handleGenerate())}
                            />
                            <Button
                                type="button"
                                variant="outline"
                                disabled={!prompt.trim() || generating}
                                onClick={handleGenerate}
                            >
                                {generating ? "…" : "Générer"}
                            </Button>
                        </div>
                    </div>
                    <form id="register-form" onSubmit={handleSubmit}>
                        <div className="flex flex-col gap-6">
                            {error && <p className="text-sm text-red-500">{error}</p>}
                            <div className="grid gap-2">
                                <Label htmlFor="username">Pseudo</Label>
                                <Input
                                    id="username"
                                    type="text"
                                    required
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                />
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="password">Mot de passe</Label>
                                <Input
                                    id="password"
                                    type="password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                        </div>
                    </form>
                </CardContent>
                <CardFooter className="flex-col gap-2">
                    <Button type="submit" form="register-form" className="w-full">
                        S'inscrire
                    </Button>
                    <p className="text-sm text-center text-muted-foreground">
                        Déjà un compte ? <Link to="/login" className="underline">Se connecter</Link>
                    </p>
                </CardFooter>
            </Card>
        </div>
    )
}
