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

export default function Register() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const navigate = useNavigate()

    async function handleSubmit(e) {
        e.preventDefault()
        setError("")
        try {
            const res = await fetch("http://localhost:8000/registration", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            })
            const data = await res.json()
            if (!res.ok) {
                setError(data.detail || "Erreur lors de l'inscription")
                return
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
                    <form id="register-form" onSubmit={handleSubmit}>
                        <div className="flex flex-col gap-6">
                            {error && <p className="text-sm text-red-500">{error}</p>}
                            <div className="grid gap-2">
                                <Label htmlFor="username">Pseudo</Label>
                                <Input
                                    id="username"
                                    type="text"
                                    placeholder="votre pseudo"
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
