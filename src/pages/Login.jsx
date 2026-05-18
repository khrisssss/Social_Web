import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { Link } from "react-router-dom"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function Login() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const navigate = useNavigate()

    async function handleSubmit(e) {
        e.preventDefault()
        setError("")
        try {
            const res = await fetch(`${import.meta.env.VITE_URL_API}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            })
            const data = await res.json()
            console.log("data: ", data)
            if (!res.ok) {
                setError(data.detail || "Erreur de connexion")
                return
            }
            localStorage.setItem("token", data.access_token)
            navigate("/")
        } catch {
            setError("Impossible de contacter le serveur")
        }
    }

    return (
        <div className="flex min-h-screen items-center justify-center">
            <Card className="w-full max-w-sm">
                <CardHeader>
                    <CardTitle>Connexion</CardTitle>
                    <CardDescription>Entrez vos identifiants pour vous connecter</CardDescription>
                </CardHeader>
                <CardContent>
                    <form id="login-form" onSubmit={handleSubmit}>
                        <div className="flex flex-col gap-6">
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
                                <div className="flex items-center">
                                    <Label htmlFor="password">Mot de passe</Label>
                                </div>
                                <Input
                                    id="password"
                                    type="password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                            {error && <p className="text-sm text-red-500">{error}</p>}

                        </div>
                    </form>
                </CardContent>
                <CardFooter className="flex-col gap-2">
                    <Button type="submit" form="login-form" className="w-full">
                        Se connecter
                    </Button>
                    <p className="text-sm text-center text-muted-foreground">
                        Pas de compte ? <Link to="/register" className="underline">Créer un compte</Link>
                    </p>
                </CardFooter>
            </Card>
        </div>
    )
}
