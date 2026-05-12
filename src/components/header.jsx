import { Button } from "@/components/ui/button"


const Header = ({ logout }) => {
    return (
        <header className="w-full z-50 bg-white border-b shadow-sm fixed mb-2.5">
            <div className="flex items-center justify-between px-6 py-4">
                <h1 className="text-3xl font-bold font-[Fredoka]">
                    TruitR
                </h1>

                <Button
                    variant="outline"
                    size="sm"
                    onClick={logout}
                >
                    Déconnexion
                </Button>
            </div>
        </header>
    );
};

export default Header;