import tractian from '../assets/tractian.png';


const NavBar = () => {
    return (
        <div
            className="w-full h-16 bg-[#454757] flex items-center justify-between px-4"
        >
            <img src={tractian} alt="Tractian" className="h-16"/>
            <div className="flex items-center gap-5">
                <div className="text-white">Logout</div>
                <div className="flex justify-center items-center rounded-full bg-[#36B6C0] h-10 w-10" >J</div>
            </div>
        </div>
    )

}

export default NavBar;